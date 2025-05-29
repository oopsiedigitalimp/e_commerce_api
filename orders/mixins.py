from .models import Order

class OrderQuerysetRoleBasedMixin:
    def get_queryset(self):
        user = self.request.user

        if getattr(user, 'is_superuser', False) or getattr(user, 'role', 'Customer') == 'Admin':
            return Order.objects.all()
        return Order.objects.filter(user=user)