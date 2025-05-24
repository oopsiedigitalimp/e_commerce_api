import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')

    class Meta:
        model = Product
        fields = ['price_min', 'price_max', 'category', 'in_stock']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        else:
            return queryset.filter(stock=0)
        
    #
    # ДОБАВИТЬ ФИЛЬТРАЦИЮ НЕ ТОЛЬКО ПО КОНЕЧНОЙ НО И ПО ОБЩИМ КАТЕГОРИЯМ
    #