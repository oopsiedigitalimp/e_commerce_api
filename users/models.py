import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = None
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    class RoleChoices(models.TextChoices):
        ADMIN = "Admin"
        EMPLOYEE = "Employee"
        CUSTOMER = "Customer"

    display_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)
    is_verified = models.BooleanField(blank=True, default=False)
    
    # TO DO: Add phone number field and authorization with django-phonenumber-field package
    # from phonenumber_field.modelfields import PhoneNumberField
    # phone_number = PhoneNumberField(blank=True, null=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        if self.display_name:
            return f"User: {self.display_name}"
        else:
            return f"User: {self.first_name} {self.last_name}"