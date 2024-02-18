"""
this file is used to store a user related data
"""
from rest_framework import routers
from django.urls import path, include

from apps.account.views import UserProfileViewSet, UserAddressViewSet, UserSettingViewSet

router = routers.DefaultRouter()

router.register('user-profile', UserProfileViewSet, basename='user_profile')
router.register('user-address', UserAddressViewSet, basename='user-address')
router.register('user-setting', UserSettingViewSet, basename='user-setting')
urlpatterns = [
    path(r'account/', include(router.urls)),
]