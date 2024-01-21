"""
this file is used to store a user related data
"""
from rest_framework import routers
from django.urls import path, include

from apps.account.views import UserProfileViewSet, UserAddressViewSet

router = routers.DefaultRouter()

router.register('user-profile', UserProfileViewSet, basename='user_profile')
router.register('user-address', UserAddressViewSet, basename='user-address')
urlpatterns = [
    path(r'account/', include(router.urls)),
]