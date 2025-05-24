from rest_framework import serializers
from .models import Product

class AdminProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d.%m.%Y at %H:%M")
    last_updated_at = serializers.DateTimeField(format="%d.%m.%Y at %H:%M")

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'category',
            'stock',
            'article_number',
            'in_stock',
            'created_at',
            'last_updated_at'
        )

    def get_category(self, obj):
        return obj.category.get_full_path()
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Price can't be lower than 0."
            )
        
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Stock can't be lower than 0."
            )
        
        return value
        
class EmployeeProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d.%m.%Y at %H:%M")
    last_updated_at = serializers.DateTimeField(format="%d.%m.%Y at %H:%M")

    class Meta:
        model = Product
        fields = (
            'name',
            'price',
            'category',
            'stock',
            'article_number',
            'in_stock',
            'created_at',
            'last_updated_at'
        )

    def get_category(self, obj):
        return obj.category.get_full_path()

class CustomerProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'price',
            'category',
            'article_number',
            'in_stock',
        )

    def get_category(self, obj):
        return obj.category.get_full_path()