import uuid

from django.db import models

# Create your models here.
from apps.authentication.models import User
from apps.common.constant import AWS_BASE_URL


class UserProfile(models.Model):
    """
    this class is used to store a user profile data
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user_profile = models.FileField(upload_to='user_profile', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='user_profile_set', )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def profile(self):
        """
        get user profile
        """
        user_profile = self.user_profile
        user_profile_url = AWS_BASE_URL + str(user_profile)
        return user_profile_url

    class Meta:
        """
        this class is used for user_profile
        """
        db_table = 'user_profile'


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address_set')
    latitude = models.CharField(max_length=1024, null=True, blank=True)
    longitude = models.CharField(max_length=1024, null=True, blank=True)
    street_address = models.CharField(max_length=1024, null=True, blank=True)
    town = models.CharField(max_length=1024, null=True, blank=True)
    phone = models.CharField(max_length=1024, null=True, blank=True)
    landmark = models.CharField(max_length=1024, null=True, blank=True)
    pincode = models.CharField(max_length=1024, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        """
        this class is used for user_profile
        """
        db_table = 'user_address'


class UserSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_setting_set')
    is_offer_notification = models.BooleanField(default=True)
    is_all_notification = models.BooleanField(default=True)
    is_payment_secure = models.BooleanField(default=False)
    is_pin_set = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_setting'
