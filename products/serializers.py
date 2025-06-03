from rest_framework import serializers
from .models import Product, ProductCategory

class AdminProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(), write_only=True
    )
    created_at = serializers.DateTimeField(format="%d.%m.%Y at %H:%M", read_only=True)
    last_updated_at = serializers.DateTimeField(format="%d.%m.%Y at %H:%M", read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'category',
            'category_id',
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
    
    def create(self, validated_data):
        category = validated_data.pop('category_id')
        product = Product.objects.create(category=category, **validated_data)
        return product
    
    def update(self, instance, validated_data):
        if 'category_id' in validated_data:
            instance.category = validated_data.pop('category_id')
        return super().update(instance, validated_data)

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
    
class ProductCategorySerializer(serializers.ModelSerializer):
    full_path = serializers.SerializerMethodField(read_only=True)
    descendants = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductCategory
        fields = (
            'name',
            'parent',
            'letter_code',
            'full_path',
            'descendants',
        )

    def get_full_path(self, obj):
        return obj.get_full_path()
    
    def get_descendants(self, obj):
        return obj.get_descendants()