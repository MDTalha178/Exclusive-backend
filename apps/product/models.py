"""
this file is used for all product which created and listed on application
file created by Md Talha
file created on : 06/12/23
"""
import uuid

from django.db import models

# Create your models here.
from apps.account.models import UserAddress
from apps.authentication.models import User
from apps.common.constant import AWS_BASE_URL


class ProductCategory(models.Model):
    """
    this table is used to create a table for product category
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_category'


class Product(models.Model):
    """
    this file is used to store a product details
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=258, null=False, blank=False)
    product_description = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    product_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='product_owner_set')
    product_active = models.BooleanField(default=False)
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, null=True, blank=True, related_name='product_category_set')
    product_quantity = models.IntegerField(default=0)
    is_in_stock = models.BooleanField(default=False)

    class Meta:
        db_table = 'product'


class ProductImages(models.Model):
    """
    this model is used to store a product images
    """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True, related_name='product_images_set')
    product_images = models.FileField(upload_to='product', null=True, blank=True)

    def get_image_url(self):
        product_images = None
        if self.product_images:
            product_images = AWS_BASE_URL + str(self.product_images)
        return product_images

    class Meta:
        """
        class meta for product images
        """
        db_table = 'product_images'


class CartItem(models.Model):
    """
    this model class is used to create a data for cart
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        this metaclass for db name
        """
        db_table = "cart_item"


class WishListItem(models.Model):
    """
    this class is used to store a wishlist data
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        this metaclass for db name
        """
        db_table = "wishlist_item"


class Order(models.Model):
    PREPARING = 'Preparing order'
    RECEIVED_AT_COURIER_OFFICE = 'Order received at courier office'
    SHIPPED = 'Order shipped'
    DELIVERED = 'Delivered'

    ORDER_STATUS_CHOICES = [
        (PREPARING, 'Preparing order'),
        (RECEIVED_AT_COURIER_OFFICE, 'Order received at courier office'),
        (SHIPPED, 'Order shipped'),
        (DELIVERED, 'Delivered'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.CharField(max_length=1024, null=False, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_order_set')
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_product_set'
    )
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(
        UserAddress, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_address_set'
    )
    combine_order_id = models.CharField(max_length=526, null=True, blank=True)
    order_status = models.CharField(max_length=1024, choices=ORDER_STATUS_CHOICES, default=PREPARING)

    class Meta:
        db_table = 'order'


class OrderBill(models.Model):
    COD = 'Cash on Delivery'
    BANK = 'Bank'
    MODE_OF_PAYMENT = [
        (COD, 'Cash on Delivery'),
        (BANK, 'Bank')
    ]
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_bill_order'
    )
    mode_of_payment = models.CharField(max_length=1024, choices=MODE_OF_PAYMENT, null=True, blank=True, default=None)
    delivery_charge = models.IntegerField(default=0)
    single_product_price = models.IntegerField(default=0)
    total_billed = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = 'order_bill'
