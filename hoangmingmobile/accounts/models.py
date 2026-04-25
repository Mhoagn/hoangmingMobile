from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email là bắt buộc')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN    = 'admin',    'Quản trị viên'
        CUSTOMER = 'customer', 'Khách hàng'

    email        = models.EmailField(unique=True)
    full_name    = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    role         = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'email'

    objects = UserManager()

    # Helper properties cho dễ kiểm tra
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER

    def __str__(self):
        return self.email

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    street = models.TextField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.street}, {self.ward}"