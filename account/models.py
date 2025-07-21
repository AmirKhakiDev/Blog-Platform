from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from .manager import AuthorManager
from django.db import models


class Author(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = AuthorManager()

    def __str__(self):
        return self.username
