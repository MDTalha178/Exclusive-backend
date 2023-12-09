from django.contrib import admin

# Register your models here.
from apps.authentication.models import User


class AdminUserDisplay(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')


admin.site.register(User, AdminUserDisplay)
