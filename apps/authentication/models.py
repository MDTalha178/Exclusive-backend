"""
This file is used to create table into database
File Created by : Md Talha
Created on: 12/03/2023
Timing: 12:07
"""

# Third Party Imports
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Local imports
from apps.authentication.managers import CustomUserManager


# Create your models here.
class UserType(models.Model):
    """
    This class is used to create table into database
    Description: this is used to store about what user is this like customer, retailer, admin etc
    """
    name = models.CharField(max_length=128, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        """
        class meta for user type
        """
        db_table = "user_type"


class User(AbstractBaseUser, PermissionsMixin):
    """
    This class is used to create a table into database
    Description: This Table is used to store basic information about User those who will log in
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=128, blank=True)
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_verification_otp = models.CharField(max_length=6, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='user_user_tye_Set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        """class meta for user"""
        db_table = 'auth_user'
