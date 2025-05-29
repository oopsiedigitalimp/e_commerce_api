from rest_framework.serializers import ModelSerializer
from .models import Order, OrderItem
from products.serializers import CustomerProductSerializer

class OrderItemSerializer(ModelSerializer):
    product = CustomerProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quantity',
            'get_subtotal'
        )

class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'customer_first_name',
            'customer_last_name',
            'comment',
            'shipping_address',
            'status',
            'created_at',
            'last_updated_at',
            'items',
            'total_price',
        )    