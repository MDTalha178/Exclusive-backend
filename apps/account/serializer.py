"""
this file is used to serialized user profile
"""
import logging

from rest_framework import serializers

from apps.account.models import UserProfile, UserAddress


class UserProfileSerializer(serializers.ModelSerializer):
    user_profile = serializers.FileField(required=False, allow_null=True, allow_empty_file=True)

    def create(self, validated_data):
        try:
            login_user_id = None
            if 'login_user_id' in self.context and self.context['login_user_id']:
                login_user_id = self.context['login_user_id']
            if not login_user_id:
                raise serializers.ValidationError({'INVALID_LOGIN': 'UNAUTHORIZED User'})
            user_profile_obj = UserProfile.objects.create(
                user_id=login_user_id, user_profile=validated_data['user_profile']
            )
            return user_profile_obj
        except Exception as e:
            logging.error(e)
            raise serializers.ValidationError(e)

    class Meta:
        model = UserProfile
        fields = ('user_profile',)


class GetUserProfileSerializer(serializers.ModelSerializer):
    """
    this class is used to get user profile
    """

    class Meta:
        model = UserProfile
        fields = ('user_profile', 'profile',)


class UserAddressSerializer(serializers.ModelSerializer):
    latitude = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    longitude = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    street_address = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    town = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    phone = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    landmark = serializers.CharField(required=False, allow_null=False, allow_blank=False)
    pincode = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    is_default = serializers.BooleanField(default=True)

    def create(self, validated_data):
        login_user_id = None
        address_id = None
        if 'login_user' in self.context and self.context['login_user']:
            login_user_id = self.context['login_user']
        if 'address_id' in self.context and self.context['address_id']:
            address_id = self.context['address_id']
        try:
            if not login_user_id:
                raise serializers.ValidationError({'UnAuthorized': 'UnAuthorized User'})
            address = UserAddress.objects.filter(user_id=login_user_id)
            if address:
                address.update(is_default=False)
            address_obj, _ = UserAddress.objects.update_or_create(
                user_id=login_user_id, id=address_id, defaults={
                    'latitude': validated_data['latitude'], 'longitude': validated_data['longitude'], 'street_address':
                        validated_data['street_address'], 'town': validated_data['town'],
                    'phone': validated_data['phone'],
                    'pincode': validated_data['pincode'], 'is_default': validated_data['is_default']
                }
            )
            return address_obj
        except Exception as e:
            logging.error(e)
            raise serializers.ValidationError(e)

    class Meta:
        model = UserAddress
        fields = ('latitude', 'longitude', 'street_address', 'town', 'phone', 'landmark', 'pincode', 'is_default')


class GetUserAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = '__all__'
