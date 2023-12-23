import logging
from datetime import datetime
from rest_framework import serializers
from django.db.models import F

from apps.common.constant import AWS_BASE_URL
from apps.product.models import Product, ProductImages, ProductCategory, CartItem


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


class AddToCartSerializer(serializers.ModelSerializer):
    """
    this class is used to create a data for cart
    """
    product = serializers.PrimaryKeyRelatedField(
        required=True, allow_null=False, allow_empty=False, queryset=Product.objects.filter())
    quantity = serializers.IntegerField(
        required=False, allow_null=True, default=1
    )

    def create(self, validated_data):
        """
        this method is used to create a cart data
        """
        try:
            login_user = None
            if 'user' in self.context and self.context['user']:
                login_user = self.context['user']
            if not login_user:
                raise serializers.ValidationError({'UnAuthorized': 'Please to login add item in to cart'})
            validated_data['user_id'] = login_user.id
            cart_obj, _ = CartItem.objects.update_or_create(
                product_id=validated_data['product'].id, user_id=login_user.id,
                defaults={'quantity': validated_data['quantity']}
            )
            return cart_obj
        except Exception as e:
            logging.error(e)
            raise serializers.ValidationError(e)

    class Meta:
        model = CartItem
        fields = ('product', 'quantity',)


class GetCartItemSerializer(serializers.ModelSerializer):
    """
    this class is used to get cart item
    """
    product_details = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    totalcart = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    total_billed = serializers.SerializerMethodField()

    def get_total_billed(self, obj):
        """
        this method is use dto get total billed
        """
        total_billed = 0
        if 'total_billed' in self.context and self.context['total_billed']:
            total_billed = self.context['total_billed']
        return total_billed


    @staticmethod
    def get_subtotal(obj):
        """
        this method is used to return total bill value
        """
        subtotal = obj.quantity * obj.product.price
        return subtotal

    @staticmethod
    def get_totalcart(obj):
        """
        this method is used to get total cart method
        """
        totalcart = CartItem.objects.filter(user_id=obj.user.id).count()
        return totalcart


    @staticmethod
    def get_product_image(obj):
        """
        get product image
        """
        product_image = None
        if hasattr(obj, 'product_image_url') and obj.product_image_url:
            product_image = AWS_BASE_URL + str(obj.product_image_url)
        return product_image

    @staticmethod
    def get_product_details(obj):
        """
        this method is used to return product details
        """
        product_details = None
        if obj.product:
            product_details = GetProductSerializer(obj.product, many=False).data
        return product_details

    class Meta:
        """
        this method is used to get product details
        """
        model = CartItem
        fields = ('product_details', 'product_image', 'quantity', 'subtotal', 'totalcart', 'total_billed',)
