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
from apps.product.views import ProductViewSet, ProductCategoryViewSet

router = routers.DefaultRouter()

router.register('product', ProductViewSet, basename='product')
router.register('product-category', ProductCategoryViewSet, basename='product_category')

urlpatterns = [
    path(r'product/', include(router.urls)),
]
