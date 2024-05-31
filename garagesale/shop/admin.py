from django.contrib import admin
from django.http import HttpRequest
from parler.admin import TranslatableAdmin
from .models import Category, Product, ProductImage, Order

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    inlines = [ProductImageInline]

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'is_cover']
    list_filter = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'first_name','last_name', 'email', 'phone', 'address','comment', 
                    'settled','created','updated',]
    list_filter = ['settled', 'created','updated']
    