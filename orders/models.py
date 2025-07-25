import uuid
from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = "New" # Customer placed a new order
        PENDING = "Pending" # System awaits payment
        PAID = "Paid" # Customer paid, order awaits delivery
        IN_DELIVERY = "In Delivery" # All items packed and on the way to the customer
        SHIPPED = "Shipped" # Order came to the destination
        CONFIRMED = "Confirmed" # Customer has confirmed recieving
        CANCELLED = "Cancelled" # Order was cancelled on any of the given stages

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    customer_first_name = models.CharField(max_length=200, default='Noname')
    customer_last_name = models.CharField(max_length=200, default='Noname')
    shipping_address = models.CharField(max_length=500)
    customer_email = models.EmailField(blank=False, null=False, default='')

    products = models.ManyToManyField('products.Product', through='OrderItem', related_name="orders")
    status = models.CharField(max_length=15, choices=StatusChoices.choices, default=StatusChoices.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.user:
            return f"Order {self.id} by {self.user}."
        else:
            return f"Order {self.id} by deleted user."

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def get_subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product} in order {self.order}"