from rest_framework import serializers
from .models import CartItem, Cart
# from products.models import Product
from products.serializers import CustomerProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = CustomerProductSerializer()

    class Meta:
        model = CartItem
        fields = (
            'product',
            'quantity',
            'get_subtotal'
        )

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            'session_key',
            'user',
            'items',
            'get_total',
            'is_active',
        )