import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from products.models import Product, ProductCategory

@pytest.mark.django_db
def test_product_list_success():
    client = APIClient()

    admin = User.objects.create_user(email='admin@test.com', password="12345", role='Admin')
    client.force_authenticate(user=admin)

    category = ProductCategory.objects.create(name="category1", letter_code="ZZ")
    Product.objects.create(name='Product1', description="It is a great product!", price=1.99, category=category)
    Product.objects.create(name='Product2', description="It is a great product!", price=1.99, category=category)

    url = reverse('products:items:product-list')
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data['count'] == 2
    