from .models import Order
from users.models import User

class OrderQuerysetRoleBasedMixin:
    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Order.objects.none()

        if getattr(user, 'is_superuser', False) or getattr(user, 'role', User.RoleChoices.CUSTOMER) == User.RoleChoices.ADMIN:
            return Order.objects.all()
        return Order.objects.filter(user=user)