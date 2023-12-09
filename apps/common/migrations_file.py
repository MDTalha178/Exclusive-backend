"""
this file is used to create predata for user
"""
from apps.authentication.commonViewSet import ModelViewSet, custom_response
from apps.product.models import ProductCategory
from rest_framework import status


class CreateProductCategory(ModelViewSet):
    """
    this is sued create a predata for user
    """
    http_method_names = ('post',)
    queryset = ProductCategory

    def create(self, request, *args, **kwargs):
        category_list = ['Woman’s Fashion', 'Men’s Fashion', 'Electronics', 'Home & Lifestyle',
                         'Medicine', 'Sports & Outdoor', 'Baby’s & Toys',
                         'Groceries & Pets', 'Health & Beauty'
                         ]
        for category in category_list:
            ProductCategory.objects.update_or_create(
                name=category, defaults={'status': 1}
            )
        return custom_response(status=status.HTTP_200_OK, detail=None, data=None)
