from rest_framework import serializers
from .models import CartItem, Cart
from products.models import Product
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

class CartItemOperationSerializator(serializers.Serializer):
    product_id = serializers.UUIDField(required=False)
    product_article_number = serializers.CharField(required=False)
    quantity = serializers.IntegerField(required=False, default=1)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Quantity must be a positive integer.')
        return value
    
    def validate(self, attrs):
        product_id = attrs.get('product_id')
        product_article_number = attrs.get('product_article_number')

        if not product_id and not product_article_number:
            raise serializers.ValidationError("Either product_id or product_article_number is required.")
        
        try:
            if product_id:
                product = Product.objects.get(id=product_id)
            else:
                product = Product.objects.get(article_number=product_article_number)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")

        attrs['product'] = product
        return attrs