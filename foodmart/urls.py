from django.urls import path
from . import views

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('update-cart-ajax/<int:product_id>/', views.update_cart_ajax, name='update_cart_ajax'),
    path('remove-cart/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.search_products, name='search'),
    path('signup/', views.signup, name='signup'),
    path("order/", views.my_orders, name="order"),
    path('payment/', views.payment_page, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('', include(router.urls)),


]

