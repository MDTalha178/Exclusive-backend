from django.contrib import admin

# Register your models here.
from apps.product.models import ProductCategory, Product, ProductImages, CartItem

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductImages)
admin.site.register(CartItem)