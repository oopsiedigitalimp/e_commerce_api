from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem

@receiver(user_logged_in)
def merge_carts_on_login(self, request, user, **kwargs):
    anonym_cart = request.cart
    user_cart, _ = Cart.objects.get_or_create(user=user, is_active=True)

    if anonym_cart.user is None and anonym_cart != user_cart and anonym_cart.items.exists():
        for item in anonym_cart.items.all():
            existing_item  = user_cart.items.filter(product=item.product).first()
            
            if existing_item:
                existing_item.quantity += item.quantity
                existing_item.save()
            else:
                item.pk = None
                item.cart = user_cart
                item.save()

    anonym_cart.is_active = False
    anonym_cart.save()
        