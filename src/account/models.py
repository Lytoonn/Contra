"""
See:
    https://docs.djangoproject.com/en/5.1/topics/db/models/
    https://docs.djangoproject.com/en/5.1/topics/db/models/#quick-example

    https://docs.djangoproject.com/en/5.1/topics/auth/
    https://docs.djangoproject.com/en/5.1/topics/auth/customizing/
    https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#writing-a-custom-user-model
    https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#a-full-example
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager

FIRST_NAME_MAXLEN = 100
LAST_NAME_MAXLEN = 160

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name = 'email address'
    )
    firstName = models.CharField(
        max_length = FIRST_NAME_MAXLEN,
        verbose_name = 'first name'
    )
    lastName = models.CharField(
        max_length = LAST_NAME_MAXLEN,
        verbose_name = 'last name'
    )
    is_active = models.BooleanField(
        default = True
    )
    is_staff = models.BooleanField(
        default = False
    )
    dateJoined = models.DateTimeField(
        default = timezone.now
    )

    is_writer = models.BooleanField(
        default = False,
        verbose_name = 'User is a writer?'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
    