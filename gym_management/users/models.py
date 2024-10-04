# users/models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, name, role, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Users must have a phone number')
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')
        if not role:
            raise ValueError('Users must have a role')

        email = self.normalize_email(email)
        user = self.model(
            phone_number=phone_number,
            email=email,
            name=name,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, name, role='manager', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, email, name, role, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('gym_owner', 'Gym Owner'),
        ('trainer', 'Trainer'),
        ('customer', 'Customer'),
        ('manager', 'Manager'),
    )
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'name', 'role']

    objects = UserManager()

    def __str__(self):
        return f"{self.name} ({self.role})"
