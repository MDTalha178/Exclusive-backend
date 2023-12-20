"""
This file is used for urls or creating endpoint for API'S
"""
# Third party imports
from django.urls import path, include
from rest_framework import routers

# Local imports
from apps.authentication.views import SignupViewSet, LoginViewSet, RefreshTokenViewSet

router = routers.DefaultRouter()

router.register('signup', SignupViewSet, basename='signup')
router.register('login', LoginViewSet, basename='login')
router.register('refresh-token', RefreshTokenViewSet, basename='refresh_token')

urlpatterns = [
    path(r'auth/', include(router.urls)),
]
