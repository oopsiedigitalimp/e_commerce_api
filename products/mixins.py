from .serializers import AdminProductSerializer, EmployeeProductSerializer, CustomerProductSerializer

class RoleBasedSerializerMixin:
    def get_serializer_class(self):
        user = self.request.user

        if not user.is_authenticated:
            return CustomerProductSerializer

        if getattr(user, 'is_superuser', False) or getattr(user, 'role', None) == 'Admin':
            return AdminProductSerializer
        elif getattr(user, 'role', None) == 'Employee':
            return EmployeeProductSerializer
        elif getattr(user, 'role', None) == 'Customer':
            return CustomerProductSerializer
        return CustomerProductSerializer