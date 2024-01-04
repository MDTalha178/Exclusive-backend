"""
this file is used for all product which created and listed on application
file created by Md Talha
file created on : 06/12/23
"""
import uuid

from django.db import models

# Create your models here.
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


