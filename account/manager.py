from django.contrib.auth.models import (
    BaseUserManager
)

class AuthorManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Name is required")
        author = self.model(username=username, **extra_fields)
        author.set_password(password)
        author.save()
        return author

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username=username, password=password, **extra_fields)