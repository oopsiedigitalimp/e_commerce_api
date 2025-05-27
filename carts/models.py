from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def get_total(self):
        return sum(item.get_subtotal for item in self.items.all())
    
    def clear(self):
        self.items.all().delete()

    def __str__(self):
        return f"Cart (user={self.user}, session={self.session_key}"
    
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def get_subtotal(self):
        return self.product.price * self.quantity
    
    def save(self, *args, **kwargs):
        if self.product.stock < self.quantity:
            raise ValueError(f"You can't add more than {self.product.stock} items of this Product.")
        
        super().save(*args, **kwargs)