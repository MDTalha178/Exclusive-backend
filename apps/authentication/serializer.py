"""
This file is used serialized a data
"""
# third party imports
from rest_framework import serializers

from apps.authentication.models import User


class SignupSerializer(serializers.ModelSerializer):
    """
    this serializer class is used to serialized a signup data
    """
    first_name = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, max_length=256,
        error_messages={'FIRST_NAME_REQUIRED': "Fisr"})
    last_name = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, max_length=256,
        error_messages={'FIRST_NAME_REQUIRED': "Fisr"})
    username = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, max_length=256,
        error_messages={'FIRST_NAME_REQUIRED': "Fisr"})
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField(
        required=True, allow_null=False, allow_blank=False, max_length=256,
        error_messages={'FIRST_NAME_REQUIRED': "Fisr"}
    )
    password = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, error_messages={'FIRST_NAME_REQUIRED': "Fisr"})

    @staticmethod
    def validate_email(value):
        """
        this function is used to validate email
        """
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('EMAIL ALREADY_EXISTS')
        return value

    def to_representation(self, obj):
        """
        this method used securing password not return in response
        """
        attr = super().to_representation(obj)
        if 'password' in attr:
            attr.pop('password')
        return attr

    def create(self, validated_data):
        """
        this method is used to create a data for user
        """
        password = validated_data['password']
        user_obj = User.objects.create(**validated_data)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj

    class Meta:
        """
        meta class signup
        """
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'phone', 'username',)


class LoginSerializer(serializers.Serializer):
    """
    this serializer is used to create for login
    """
    email = serializers.EmailField(
        required=True, allow_null=False, allow_blank=False, error_messages={
            'EMAIL_FILED_REQUIRED': "Please enter your email"}
    )
    password = serializers.CharField(
        required=True, allow_blank=False, allow_null=False, error_messages={
            'PASSWORD_IS_REQUIRED': "Please enter your password"
        }
    )

    def validate(self, attrs):
        """
        this method is used for validation which validate the following details
        """
        if not User.objects.filter(email__iexact=attrs.get('email')).exists():
            raise serializers.ValidationError({'INVALID_EMAIL': "Given email address is invalid please enter a "
                                                                "valid email Address"})
        user_obj = User.objects.filter(email__iexact=attrs.get('email')).first()
        if user_obj:
            if not user_obj.check_password(attrs.get('password')):
                raise serializers.ValidationError({"INVALID_PASSWORD": "Please enter a valid password"})
        attrs.update({'user_obj': user_obj})
        return attrs

    class Meta:
        """
        class Meta for User
        """
        model = User
        fields = ('id', 'email', 'password')


class RefreshTokenSerializer(serializers.Serializer):
    """
    this class is sued to get refresh token
    """
    refresh_token = serializers.CharField(
        required=True, allow_null=False, allow_blank=False, error_messages={'Token': 'Refresh token is required!'})