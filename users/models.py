import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'Admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = None
    first_name = models.CharField(max_length=150, default="Noname")
    last_name = models.CharField(max_length=150, default="Noname")

    class RoleChoices(models.TextChoices):
        ADMIN = "Admin"
        EMPLOYEE = "Employee"
        CUSTOMER = "Customer"

    display_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)
    is_verified = models.BooleanField(blank=True, default=False)
    shipping_address = models.CharField(max_length=500, null=True)
    
    # TO DO: Add phone number field and authorization with django-phonenumber-field package
    # from phonenumber_field.modelfields import PhoneNumberField
    # phone_number = PhoneNumberField(blank=True, null=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        constraints = [
            models.CheckConstraint(condition=~models.Q(email=""), name="email_not_empty")
        ]
    
    def __str__(self):
        if self.display_name:
            return f"User: {self.display_name}, email: {self.email}"
        else:
            return f"User: {self.first_name} {self.last_name}, email: {self.email}"
