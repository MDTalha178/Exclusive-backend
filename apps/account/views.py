from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.account.models import UserAddress
from apps.account.serializer import UserProfileSerializer, UserAddressSerializer, GetUserAddressSerializer
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


class UserAddressViewSet(ModelViewSet):
    """
    this class is used to create and get user Address
    """
    http_method_names = ('get', 'post')
    queryset = UserAddress
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated, IsTokenValid,)

    def get_queryset(self):
        is_default = self.request.GET.get('is_default', None)
        if is_default:
            queryset = self.queryset.objects.filter(user_id=self.request.user.id, is_default=True)
            return queryset
        queryset = self.queryset.objects.filter(user_id=self.request.user.id)
        return queryset

    def create(self, request, *args, **kwargs):
        login_user_id = self.request.user.id
        address_id = self.request.GET.get('address_id', None)
        serializer = self.serializer_class(data=request.data, context={
            'login_user': login_user_id, 'address_id': address_id})
        if serializer.is_valid():
            serializer.save()
            return custom_response(status=status.HTTP_200_OK, detail=None, data=serializer.data)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=None,data=serializer.errors)

    def list(self, request, *args, **kwargs):
        self.serializer_class = GetUserAddressSerializer
        serializer = self.serializer_class(self.get_queryset(), many=True)
        if serializer:
            return custom_response(status=status.HTTP_200_OK, detail=None, data=serializer.data)
        return custom_error_response(status=status.HTTP_204_NO_CONTENT, detail=None, data=None)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=None, data={
                'INVALID_ID': "ADDRESS_NOT_FOUND"}
                                         )
        self.serializer_class = GetUserAddressSerializer
        serializer = self.serializer_class(instance, many=False)
        if serializer:
            return custom_response(status=status.HTTP_200_OK, detail=None, data=serializer.data)
        return custom_error_response(status=status.HTTP_204_NO_CONTENT, detail=None, data=None)
