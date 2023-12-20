"""
This file is used for signup viewset
"""
# Third party imports
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# Local Import
from apps.authentication.commonViewSet import ModelViewSet, custom_response, custom_error_response

# Create your views here.
from apps.authentication.models import User
from apps.authentication.serializer import SignupSerializer, LoginSerializer, RefreshTokenSerializer


class SignupViewSet(ModelViewSet):
    """
    this class is used for signup viewset where user can signup
    """
    http_method_names = ('post',)
    serializer_class = SignupSerializer
    queryset = User

    def create(self, request, *args, **kwargs):
        """
        this method is used to create a signup data
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # generating a token for user
            refresh_token = RefreshToken.for_user(user)
            token = dict()
            token['access_token'] = str(refresh_token.access_token)
            token['refresh_token'] = str(refresh_token)
            return custom_response(status=status.HTTP_200_OK, detail=token, data=serializer.data)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=None, data=serializer.errors)


class LoginViewSet(ModelViewSet):
    """
    this class is used for user login
    """
    http_method_names = ('post',)
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        """
        this is used to get a data
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.validated_data.get('user_obj')
            # here we will generate a JWT token for user
            refresh_token = RefreshToken.for_user(user_obj)
            response = dict()
            response['access_token'] = str(refresh_token.access_token)
            response['refresh_token'] = str(refresh_token)
            return custom_response(status=status.HTTP_200_OK, detail=None, data=response)
        return custom_error_response(status=status.HTTP_401_UNAUTHORIZED, detail=None, data=serializer.errors)


class RefreshTokenViewSet(ModelViewSet):
    """
    this class is sued to get refresh token
    """
    http_method_names = ('post',)
    serializer_class = RefreshTokenSerializer

    def create(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return custom_error_response(
                status=status.HTTP_400_BAD_REQUEST, detail=None, data='Refresh token is required'
            )
        try:
            refresh_token = RefreshToken(refresh_token)
            access_token = str(refresh_token.access_token)
            new_refresh_token = str(refresh_token)
            return custom_response(status=status.HTTP_200_OK, detail=None, data=
            {'access_token': access_token, 'refresh_token': new_refresh_token})
        except Exception as e:
            return custom_response(status=status.HTTP_401_UNAUTHORIZED, detail={'detail': str(e)}, data=None)
