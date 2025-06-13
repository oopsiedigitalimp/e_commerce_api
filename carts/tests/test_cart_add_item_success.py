import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from products.models import Product, ProductCategory
from carts.models import Cart

@pytest.mark.django_db
def test_cart_add_item_by_id_success():
    client = APIClient()

    admin = User.objects.create_superuser(email='admin@test.com', password="12345")
    client.force_authenticate(user=admin)

    category = ProductCategory.objects.create(name="category1", letter_code="ZZ")
    product = Product.objects.create(name="Product", description="This is a great product!", price=13.99, category=category, stock=10)

    payload = {
        'product_id': product.id
    }

    url = reverse('carts:cart-detail')
    response = client.post(url, payload)
    
    print(response.data)
    assert response.status_code == 201
    assert response.data['product']['article_number'] == product.article_number

@pytest.mark.django_db
def test_cart_add_item_by_article_number_success():
    client = APIClient()

    admin = User.objects.create_superuser(email='admin@test.com', password="12345")
    client.force_authenticate(user=admin)

    category = ProductCategory.objects.create(name="category1", letter_code="ZZ")
    product = Product.objects.create(name="Product", description="This is a great product!", price=13.99, category=category, stock=10)

    payload = {
        'product_articl_number': product.article_number
    }

    url = reverse('carts:cart-detail')
    response = client.post(url, payload)
    
    print(response.data)
    assert response.status_code == 201
    assert response.data['product']['article_number'] == product.article_number