from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.conf import settings

from .models import Category, SubCategory, Product, Cart, CartItem, Order, OrderItem, UserProfile

import json
import razorpay


# ================= CART =================
def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


# ================= HOME =================
def home(request):
    categories = Category.objects.all()

    category_products = []
    for category in categories:
        products = Product.objects.filter(subcategory__category=category)[:10]
        category_products.append({
            'category': category,
            'products': products
        })

    return render(request, 'home.html', {
        'categories': categories,
        'category_products': category_products
    })


# ================= PROFILE SIGNAL =================
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# ================= PROFILE =================
@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    orders = Order.objects.filter(user=request.user)\
        .prefetch_related('items__product')\
        .order_by("-created_at")

    if request.method == "POST":
        profile.name = request.POST.get("name")
        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")

        if request.FILES.get("image"):
            profile.image = request.FILES["image"]

        profile.save()

    return render(request, "profile.html", {
        "profile": profile,
        "orders": orders
    })


# ================= CATEGORY =================
def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategory_slug = request.GET.get('subcategory')

    if subcategory_slug:
        subcategory = get_object_or_404(SubCategory, slug=subcategory_slug, category=category)
        products = Product.objects.filter(subcategory=subcategory)
    else:
        products = Product.objects.filter(subcategory__category=category)

    return render(request, 'category_products.html', {
        'category': category,
        'products': products,
        'subcategories': category.subcategories.all(),
        'selected_subcategory': subcategory_slug,
    })


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    return render(request, 'product_detail.html', {'product': product})


# ================= CART =================
# def add_to_cart(request, product_id):
#     if request.method == "POST":
#         product = Product.objects.get(id=product_id)

#         cart = get_cart(request)

#         cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
#         cart_item.quantity += 1
#         cart_item.save()

#         return JsonResponse({
#             "quantity": cart_item.quantity,
#             "cart_count": cart.items.count()
#         })


def add_to_cart(request, product_id):
    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        cart = get_cart(request)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += 1  # only increase if already exists

        cart_item.save()

        return JsonResponse({
            "quantity": cart_item.quantity,
            "cart_count": cart.items.count()
        })

def update_cart_ajax(request, product_id):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")

        cart = get_cart(request)

        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)

        if action == "increase":
            cart_item.quantity += 1

        elif action == "decrease":
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
                return JsonResponse({"quantity": 0, "cart_count": 0})

        cart_item.save()

        return JsonResponse({
            "quantity": cart_item.quantity,
            "cart_count": cart.items.count()
        })


def cart_view(request):
    cart = get_cart(request)
    items = cart.items.select_related('product').all()
    total = sum(item.total_price() for item in items)

    return render(request, 'cart.html', {'items': items, 'total': total})


def remove_cart_item(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id)
        item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart_view')


# ================= CHECKOUT =================
@login_required
def checkout(request):

    cart = get_cart(request)
    items = cart.items.select_related('product').all()

    cart_items = []
    total = 0

    for item in items:
        subtotal = item.product.effective_price * item.quantity
        total += subtotal

        cart_items.append({
            "product": item.product,
            "quantity": item.quantity,
            "price": item.product.effective_price,
            "subtotal": subtotal
        })

    if request.method == "POST":

        order = Order.objects.create(
            user=request.user,
            total_price=total,
            is_paid=False
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.effective_price
            )

        request.session['order_id'] = order.id

        return redirect('payment')

    return render(request, "checkout.html", {
        "items": cart_items,
        "total": total
    })




# PAYMENT 
@login_required
def payment_page(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)

    amount = int(order.total_price * 100)

    import razorpay
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    razorpay_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    order.razorpay_order_id = razorpay_order['id']
    order.save()

    return render(request, "payment.html", {
        "order": order,
        "razorpay_order_id": razorpay_order['id'],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount
    })



# ================= PAYMENT SUCCESS =================
@login_required
def payment_success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')

    import razorpay
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        order = Order.objects.get(razorpay_order_id=order_id)
        order.razorpay_payment_id = payment_id
        order.is_paid = True
        order.save()

        cart = get_cart(request)
        items = cart.items.select_related('product').all()

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.effective_price
            )

        items.delete()

        return redirect('profile')

    except Exception as e:
        print(e)
        return redirect('payment_failed')


def payment_failed(request):
    return render(request, "payment_failed.html")

@login_required
def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order.status = 'cancelled'
    order.save()
    return redirect('profile')

# ================= SEARCH =================
def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else []

    return render(request, 'search.html', {'query': query, 'products': products})


# ================= AUTH =================
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully ")
            return render(request, 'signup.html', {'form': UserCreationForm()})
        else:
            messages.error(request, "Please fix the errors below ")
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_orders.html", {"orders": orders})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

# api
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

#viewset-Full CRUD API
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

