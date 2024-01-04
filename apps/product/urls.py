"""
this file is use for product
"""
"""
This file is used for urls or creating endpoint for API'S
"""
# Third party imports
from django.urls import path, include
from rest_framework import routers

# Local imports
from apps.product.views import ProductViewSet, ProductCategoryViewSet, CartViewSet, WishListViewSet

router = routers.DefaultRouter()

router.register('product', ProductViewSet, basename='product')
router.register('product-category', ProductCategoryViewSet, basename='product_category')
router.register('cart', CartViewSet, basename='cart')
router.register('add-wishlist', WishListViewSet, basename='add_wishlist')
urlpatterns = [
    path(r'product/', include(router.urls)),
]
