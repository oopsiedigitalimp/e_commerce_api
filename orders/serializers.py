from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import CustomerProductSerializer
from users.models import User

class OrderItemSerializer(serializers.ModelSerializer):
    product = CustomerProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quantity',
            'get_subtotal'
        )

class OrderSerializer(serializers.ModelSerializer):
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

class CreateOrderSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    shipping_address = serializers.CharField()
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        request = self.context['request']
        cart = request.cart

        if not cart.items.exists():
            raise serializers.ValidationError("Cart is empty.")
        
        for item in cart.items.all():
            if item.quantity > item.product.quantity:
                raise serializers.ValidationError({
                "error": "Недостаточно товара на складе",
                "product": item.product.name,
                "available": item.product.quantity,
                "requested": item.quantity
            })

        return 
    
    def create(self, validated_data):
        request = self.context['request']
        cart = request.cart

        if request.user.is_authenticated:
            user = cart.user
        else:
            user = None

        order = Order.objects.create(
            user=user,
            customer_first_name=validated_data.get('first_name'),
            customer_last_name=validated_data.get('last_name'),
            customer_email=validated_data.get('email'),
            shipping_address=validated_data.get('shipping_address'),
            comment=validated_data.get('comment', ''),
            total_price=cart.get_total,
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        cart.clear()
        cart.is_active = False
        cart.save()

        return order