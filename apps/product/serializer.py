import logging
from datetime import datetime
from rest_framework import serializers
from django.db import transaction

from apps.account.models import UserAddress
from apps.account.serializer import GetUserAddressSerializer
from apps.common.constant import AWS_BASE_URL
from apps.common.utils import get_order_id, get_combine_order_id
from apps.product.models import Product, ProductImages, ProductCategory, CartItem, WishListItem, Order, OrderBill


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
            is_cart = self.context['is_cart']
            if 'user' in self.context and self.context['user']:
                login_user = self.context['user']
            if not login_user:
                raise serializers.ValidationError({'UnAuthorized': 'Please to login add item in to cart'})
            validated_data['user_id'] = login_user.id
            if is_cart:
                product_id = validated_data['product_id'].id
                user_id = login_user.id
                cart_obj, created = CartItem.objects.get_or_create(
                    product_id=product_id, user_id=user_id,
                    defaults={'quantity': validated_data['quantity']}
                )
                if not created:
                    cart_obj.quantity += 1
                    cart_obj.save()
                    WishListItem.objects.filter(
                        product_id=product_id, user_id=user_id
                    ).delete()
            elif int(validated_data['quantity']) == 0:
                CartItem.objects.filter(product_id=validated_data['product'].id, user_id=login_user.id).delete()
                cart_obj = CartItem.objects.filter(user_id=login_user.id).first()
            else:
                cart_obj, _ = CartItem.objects.update_or_create(
                    product_id=validated_data['product'].id, user_id=login_user.id,
                    defaults={'quantity': validated_data['quantity']}
                )
            return login_user
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


class WishListItemSerializer(serializers.ModelSerializer):
    """
    this class is used to wishlist serializer
    """
    product = serializers.PrimaryKeyRelatedField(
        required=True, allow_null=False, allow_empty=False, queryset=Product.objects.filter())

    def create(self, validated_data):
        """
        this method is used to create a wishlist data
        :param validated_data
        """
        try:
            login_user = None
            if 'user' in self.context and self.context['user']:
                login_user = self.context['user']
            if not login_user:
                raise serializers.ValidationError({'UnAuthorized': 'Please to login add item in to cart'})
            validated_data['user_id'] = login_user.id
            cart_obj, _ = WishListItem.objects.update_or_create(
                product_id=validated_data['product'].id, user_id=login_user.id,
            )
            return cart_obj
        except Exception as e:
            logging.error(e)
            raise serializers.ValidationError(e)

    class Meta:
        """
        metaclass for wishlist
        """
        model = WishListItem
        fields = ('product',)


class GetWishListItemSerializer(serializers.ModelSerializer):
    """
    this serializer class is used to get wishlist data
    """
    product_details = serializers.SerializerMethodField()
    product_image_url = serializers.SerializerMethodField()

    @staticmethod
    def get_product_image_url(obj):
        product_image_url = None
        if hasattr(obj, 'product_image_url'):
            product_image_url = AWS_BASE_URL + str(obj.product_image_url)
        return product_image_url

    @staticmethod
    def get_product_details(obj):
        """
        this method is used to get product details
        """
        product_details = None
        if obj.product:
            product_details = GetProductSerializer(obj.product, many=False).data
        return product_details

    class Meta:
        model = WishListItem
        fields = ('id', 'product_details', 'product_image_url',)


class OrderPlaceSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        many=True,
        required=True,
        queryset=Product.objects.filter()
    )
    sub_total = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    total_billed = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    shipping_fee = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    mode_of_payment = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    coupon_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate(self, attrs):
        if attrs.get('sub_total') == 0:
            raise serializers.ValidationError({'BILLED_PRICE': 'Billed price is invalid'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        login_user_id = None
        order_obj = None
        if 'login_user_id' in self.context and self.context['login_user_id']:
            login_user_id = self.context['login_user_id'].id
        try:
            if not login_user_id:
                raise serializers.ValidationError({'UNAUTHORIZED_USER': "Un Authorized user"})
            user_address = UserAddress.objects.filter(user_id=login_user_id, is_default=True).first()
            if not user_address:
                raise serializers.ValidationError({'ADDRESS': "PLEASE_ADD_ADDRESS"})
            combine_order_id = get_combine_order_id()
            for product in validated_data['product']:
                order_id = get_order_id()
                cart_item = CartItem.objects.filter(product_id=product.id, user_id=login_user_id).first()
                quantity = cart_item.quantity if cart_item else 1
                order_obj = Order.objects.create(
                    user_id=login_user_id, product_id=product.id,
                    quantity=quantity, order_id=order_id,
                    address_id=user_address.id,
                    combine_order_id=combine_order_id
                )
                total_bill = product.price * quantity
                total_billed = total_bill if int(validated_data['sub_total']) > 300 else total_bill + 40
                is_paid = False if validated_data['mode_of_payment'] == 'COD' else True
                OrderBill.objects.create(
                    order_id=order_obj.id, mode_of_payment=OrderBill.COD,
                    delivery_charge=validated_data['shipping_fee'],
                    single_product_price=total_bill, total_billed=total_billed, is_paid=is_paid
                )
            CartItem.objects.filter(user_id=login_user_id).delete()
            return order_obj
        except Exception as e:
            logging.error(e)
            raise serializers.ValidationError(e)

    class Meta:
        model = Order
        fields = ('product', 'sub_total', 'total_billed', 'shipping_fee', 'mode_of_payment', 'coupon_name')


class GetOrderBillDetails(serializers.ModelSerializer):
    class Meta:
        model = OrderBill
        fields = '__all__'


class GetOrderListSerializer(serializers.ModelSerializer):
    order_bill = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    product_image_url = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    @staticmethod
    def get_full_name(obj):
        if obj.user.first_name and obj.user.last_name:
            full_name = obj.user.last_name + " " + obj.user.last_name
        else:
            full_name = obj.user.username
        return full_name

    @staticmethod
    def get_shipping_address(obj):
        shipping_address = None
        address_obj = UserAddress.objects.filter(id=obj.address.id).first()
        if address_obj:
            shipping_address = GetUserAddressSerializer(address_obj, many=False).data
        return shipping_address

    @staticmethod
    def get_product_image_url(obj):
        product_image_url = None
        if hasattr(obj, 'product_image_url'):
            product_image_url = AWS_BASE_URL + str(obj.product_image_url)
        return product_image_url

    @staticmethod
    def get_order_bill(obj):
        order_bill_details = None
        order_bill_details_obj = OrderBill.objects.filter(order_id=obj.id).first()
        if order_bill_details_obj:
            order_bill_details = GetOrderBillDetails(order_bill_details_obj, many=False).data
        return order_bill_details

    @staticmethod
    def get_product(obj):
        return GetProductSerializer(obj.product, many=False).data

    class Meta:
        model = Order
        fields = ('id', 'order_id', 'product', 'quantity', 'order_status',
                  'order_bill', 'product_image_url', 'created_at', 'shipping_address', 'full_name')
