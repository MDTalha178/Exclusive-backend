from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.account.serializer import UserProfileSerializer
from apps.authentication.commonViewSet import ModelViewSet, custom_response, custom_error_response
from apps.common.permissions import IsTokenValid


class UserProfileViewSet(ModelViewSet):
    """
    this class is used to create and get user profile
    """
    http_method_names = ('get', 'post',)
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, IsTokenValid,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'login_user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return custom_response(status=status.HTTP_200_OK, detail=None, data=serializer.data)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=None, data=serializer.errors)
