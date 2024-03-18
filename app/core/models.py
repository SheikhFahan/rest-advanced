"""database models"""


from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,  # func for the authentication
    PermissionsMixin,   # func for the permissions & fields
    BaseUserManager,
)
from django.conf import settings


class UserManager(BaseUserManager):
    """manager for users"""

    def create_user(self, email, password=None, **extrafields):
        """creates saves and returns a new user"""
        if not email:
            raise ValueError("User must have an email")
        user = self.model(email=self.normalize_email(email), **extrafields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extrafields):
        """create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Create user model"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # change the default authentication field to email

class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.title