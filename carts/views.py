from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import NotFound, ValidationError
from .models import CartItem, Cart
from .serializers import CartItemSerializer, CartSerializer, CartItemOperationSerializator
from products.models import Product

class CartGetChangeAPIView(APIView):
    def post(self, request):
        serializer = CartItemOperationSerializator(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        cart = request.cart
        quantity = self.validated['quantity']
        product = self.validated['product']
    
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            item.quantity += quantity
            item.save()

        serializer = CartItemSerializer(item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        serializer = CartItemOperationSerializator(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        cart = request.cart
        product = self.validated['product']

        try:
            item = CartItem.objects.get(cart=cart, product_id=product.id)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request):
        serializer = CartItemOperationSerializator(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        cart = request.cart
        product = self.validated['product']
        quantity = self.validated['quantity']

        try:
            item = CartItem.objects.get(cart=cart, product_id=product.id)
            
            if item.quantity > quantity:
                item.quantity -= quantity
                item.save()
                serializer = CartItemSerializer(item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif item.quantity == quantity:
                item.delete()
                return Response({'detail': 'Item was removed from cart.'}, status=status.HTTP_200_OK)
            else:
                raise ValidationError("Cannot remove more items than are in the cart.") 
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request):
        cart = request.cart
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CartClearAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        cart = request.cart
        cart.clear()
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        serializer = CartSerializer(request.cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartSerializer(request.cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartListAPIView(generics.ListAPIView):
    queryset = Cart.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CartSerializer