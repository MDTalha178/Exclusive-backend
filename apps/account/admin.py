from django.contrib import admin

# Register your models here.
from apps.account.models import UserProfile, UserAddress, UserSetting

admin.site.register(UserProfile)
admin.site.register(UserAddress)
admin.site.register(UserSetting)
