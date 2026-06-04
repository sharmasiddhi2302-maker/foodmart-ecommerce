from django.contrib import admin
from .models import Category, SubCategory, Product, Cart, Order,CartItem ,UserProfile
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubCategoryInline]

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'subcategory', 'price', 'quantity', 'unit')

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(UserProfile)
admin.site.register(Order)
