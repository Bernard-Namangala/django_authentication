"""
module to hold custom model managers
"""

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy


class CustomUserManager(BaseUserManager):
    """
    custom user model manager
    """
    def create_user(self, email, password, **extra_fields):
        """
        creates and saves a user with given email and password
        """
        if not email:
            raise ValueError(ugettext_lazy("Email is required"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        creates and save a super user with given email and password
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(ugettext_lazy('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(ugettext_lazy('Superuser must have is_superuser=True.'))

        user = self.create_user(email, password, **extra_fields)
        return user
        