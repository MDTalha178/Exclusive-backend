from django.contrib import admin

# Register your models here.
from apps.account.models import UserProfile, UserAddress

admin.site.register(UserProfile)
admin.site.register(UserAddress)
