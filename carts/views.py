from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import NotFound, ValidationError
from .models import CartItem, Cart
from .serializers import CartItemSerializer, CartSerializer
from products.models import Product

class CartGetChangeAPIView(APIView):
    def get_product_or_404(self, request):
        product_id = request.data.get('product_id', None)
        product_article_number = request.data.get('product_article_number', None)

        if product_id:
            try:
                return Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise NotFound('Product not found by product_id.')
            
        if product_article_number:
            try:
                return Product.objects.get(article_number=product_article_number)
            except Product.DoesNotExist:
                raise NotFound('Product not found by article_number.')
            
        raise NotFound('Product not found — no identifier provided.')

    def get_quantity_or_404(self, request):
        quantity = request.data.get('quantity', 1)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValidationError('Quantity must be a positive integer.')
        except:
            raise ValidationError('Quantity must be a positive integer.')
        
        return quantity
        

    def post(self, request):
        cart = request.cart
        quantity = self.get_quantity_or_404(request)
        product = self.get_product_or_404(request)
    
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            item.quantity += quantity
            item.save()

        serializer = CartItemSerializer(item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        cart = request.cart
        product = self.get_product_or_404(request)

        try:
            item = CartItem.objects.get(cart=cart, product_id=product.id)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request):
        cart = request.cart
        product = self.get_product_or_404(request)
        quantity = self.get_quantity_or_404(request)

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