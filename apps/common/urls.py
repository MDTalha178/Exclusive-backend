"""
This file is used for urls or creating endpoint for API'S
"""
# Third party imports
from django.urls import path, include
from rest_framework import routers

# Local imports
from apps.common.migrations_file import CreateProductCategory

router = routers.DefaultRouter()

router.register('create-category', CreateProductCategory, basename='create_category')

urlpatterns = [
    path(r'model/', include(router.urls)),
]