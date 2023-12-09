"""
this used for views
"""

from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from apps.authentication.commonViewSet import ModelViewSet, custom_response, custom_error_response
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

# Create your views here.
from apps.common.permissions import IsTokenValid
from apps.product.models import Product
from apps.product.serializer import GetProductSerializer, CreateProductSerializer


class ProductViewSet(ModelViewSet):
    """
    this method is used to get product details
    """
    http_method_names = ('get', 'post', 'delete',)
    queryset = Product
    serializer_class = GetProductSerializer
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    permission_classes = (IsAuthenticated, IsTokenValid,)

    def get_queryset(self):
        """
        this method is used to get queryset
        """
        is_seller_dashboard = self.request.query_params.get('is_seller_dashboard', 'false').lower() == 'true'
        user_id = self.request.query_params.get('user_id')
        queryset = Product.objects.annotate(
            product_image_url=F('product_images_set__product_images'),

        )
        if is_seller_dashboard:
            queryset = queryset.filter(product_owner_id=user_id)
        else:
            queryset = queryset.filter(product_active=True)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        this method is used to create product
        """
        login_user = request.user
        serializer = CreateProductSerializer(data=request.data, context={'login_user': login_user})
        if serializer.is_valid():
            serializer.save()
            return custom_response(status=status.HTTP_201_CREATED, detail=None, data=serializer.data)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=None, data=serializer.errors)

    def list(self, request, *args, **kwargs):
        """
        this method is used to get a product list
        """
        serializer = self.serializer_class(self.get_queryset(), many=True)
        if serializer:
            return custom_response(status=status.HTTP_200_OK, detail=None, data=serializer.data)
        return custom_error_response(status=status.HTTP_204_NO_CONTENT, detail=None, data=None)

    def retrieve(self, request, *args, **kwargs):
        """
        this method is to get a single product
        """
        serializer = self.serializer_class(self.get_object(), many=False)
        if serializer:
            return custom_response(status=status.HTTP_200_OK, detail=None, data=serializer.data)
        return custom_response(status=status.HTTP_204_NO_CONTENT, detail=None, data=None)

    def destroy(self, request, *args, **kwargs):
        """
        this method is used to delete a product
        """
        instance = self.get_object()
        if instance:
            instance.delete()
            return custom_response(status=status.HTTP_200_OK, detail=None, data=None)
        return custom_response(status.HTTP_204_NO_CONTENT, detail=None, data=None)
