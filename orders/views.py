from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User
from products.models import Product
from products.permissions import IsAdminOrReadOnly
from .mixins import OrderQuerysetRoleBasedMixin
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem

class OrderListAPIView(OrderQuerysetRoleBasedMixin, generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class OrderRetrieveUpdateDestroyAPIView(OrderQuerysetRoleBasedMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReadOnly]

class OrderCreateAPIView(APIView):
    def post(self, request):
        cart = request.cart
        
        if cart.items.exists():
            for item in cart.items.all():
                if item.quantity > item.product.quantity:
                    return Response({
                    "error": "Недостаточно товара на складе",
                    "product": item.product.name,
                    "available": item.product.quantity,
                    "requested": item.quantity
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user.is_authenticated:
                user = cart.user
            else:
                user, created = User.objects.get_or_create(
                    email=request.data.get('email'),
                    defaults={
                        "first_name": request.data.get("first_name", ""),
                        "last_name": request.data.get("last_name", ""),
                        "role": "Customer",
                    }
                )
                
            try:
                order = Order.objects.create(
                        user=user,
                        customer_first_name=user.first_name,
                        customer_last_name=user.last_name,
                        customer_email=user.email,
                        shipping_address=request.data.get('shipping_address'),
                        comment=request.data.get('comment'),
                        total_price=cart.get_total,
                    )
            except Exception as e:
                return Response({"error": f"Can't create order: {str(e)}"}, status=400)

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                )

            cart.clear()
            cart.is_active = False
            cart.save()

            serializer = OrderSerializer(order)

            return Response(serializer.data, status=status.HTTP_201_CREATED)