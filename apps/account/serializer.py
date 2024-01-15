"""
this file is used to serialized user profile
"""
import logging

from rest_framework import serializers

from apps.account.models import UserProfile


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