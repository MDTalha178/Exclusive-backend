import logging
from datetime import datetime
from rest_framework import serializers

from apps.common.constant import AWS_BASE_URL
from apps.product.models import Product, ProductImages, ProductCategory


class GetProductCategoryDetails(serializers.ModelSerializer):
    """
    this method is used to get product category details
    """

    class Meta:
        model = ProductCategory
        fields = '__all__'


class GetProductSerializer(serializers.ModelSerializer):
    """
    this serializer is used to get a product
    """
    product_image = serializers.SerializerMethodField()
    product_category = serializers.SerializerMethodField()

    @staticmethod
    def get_product_category(obj):
        """
        this method is used to get a product category
        """
        product_category_details = None
        if obj.product_category:
            product_category_details = GetProductCategoryDetails(obj.product_category, many=False).data
        return product_category_details

    @staticmethod
    def get_product_image(obj):
        """
        get product image
        """
        product_image = None
        if hasattr(obj, 'product_image_url') and obj.product_image_url:
            product_image = AWS_BASE_URL + str(obj.product_image_url)
        return product_image

    class Meta:
        model = Product
        fields = '__all__'


class CreateProductSerializer(serializers.ModelSerializer):
    """
    this serializer used to create a product
    """
    product_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    product_description = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    price = serializers.IntegerField(required=True, allow_null=False)
    product_quantity = serializers.IntegerField(required=True, allow_null=False)
    product_image = serializers.FileField(required=False, allow_null=True, allow_empty_file=True)
    product_active = serializers.BooleanField(required=False, allow_null=True, default=False)
    product_category = serializers.PrimaryKeyRelatedField(
        required=True, allow_null=False, allow_empty=False, queryset=ProductCategory.objects.filter()
    )
    is_in_stock = serializers.BooleanField(default=True)

    def validate(self, attrs):
        """
        this method is used to validate a data
        """
        if attrs.get('product_quantity') == 0 or not attrs.get('product_active'):
            attrs.update({'is_in_stock': False})
        return attrs

    def create(self, validated_data):
        try:
            login_user = self.context['login_user']
            product_image = validated_data['product_image']
            validated_data.pop('product_image')
            product_obj = Product.objects.create(
                **validated_data, created_at=datetime.now(), updated_at=datetime.now(),
                product_owner_id=login_user.id
            )
            ProductImages.objects.create(product_id=product_obj.id, product_images=product_image)
            return product_obj
        except Exception as e:
            logging.error(e)

    class Meta:
        model = Product
        fields = ('product_name', 'product_description', 'price', 'product_quantity', 'product_image',
                  'is_in_stock', 'product_active', 'product_category')


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
