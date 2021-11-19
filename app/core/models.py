from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                        BaseUserManager, \
                                        PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        superuser = self.create_user(email=email, password=password, **extra_fields)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self.db)

        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    """Cstom User Model that supports email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'