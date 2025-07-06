import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')
    class Meta:
        model = Order
        fields = {
            'total_price': ['lt', 'gt', 'exact', 'range'],
            'status': ['exact'],
            'created_at': ['lt', 'gt', 'exact'],
        }