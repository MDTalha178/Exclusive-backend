"""
This is used for custom manager for User
"""
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    manager for user model
    """
    use_in_migration = True

    @classmethod
    def normalize_email(cls, email):
        """
        all email is case-insensitive
        """
        email = email or ''
        return email.lower()

    def _create_user(self, email, password, **extra_fields):
        """
        create a new user and save data in database
        :param email : email
        :param password: password
        return user instance
        """
        if not email:
            raise ValueError('The given email not set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        create a super user or admin account
        :param email:email
        :param password: password
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('email_verified', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('super user must be Staff True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('super user must be Staff True')
        return self._create_user(email,password, **extra_fields)