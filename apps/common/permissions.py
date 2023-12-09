"""
this is used to verify permissions
"""
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class IsTokenValid(BasePermission):
    """
    this class is used to validate a toke
    """
    def has_permission(self, request, view):
        """
        this method will verify token is still valid or not
        """
        jwt_authenticator = JWTAuthentication()
        user, token = jwt_authenticator.authenticate(request)
        return user is not None and token is not None
