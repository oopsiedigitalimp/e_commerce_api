import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from products.models import Product, ProductCategory

@pytest.mark.django_db
def test_product_update_by_id_success():
    client = APIClient()

    admin = User.objects.create_superuser(email='admin@test.com', password="12345")
    client.force_authenticate(user=admin)

    category = ProductCategory.objects.create(name="category1", letter_code="ZZ")
    product1 = Product.objects.create(name="Product1", description="This is a great product!", price=13.99, category=category)
    product2 = Product.objects.create(name="Product2", description="This is a great product!", price=14.99, category=category)

    url = reverse('products:product-detail', kwargs={'pk': product1.id})
    response = client.get(url)

    assert response.data['name'] == "Product1"

    payload = {
        'name': "Updated Product"
    }

    response = client.patch(url, payload)

    assert response.status_code == 200
    assert response.data['name'] == payload['name']

@pytest.mark.django_db
def test_product_update_by_article_number_success():
    client = APIClient()

    admin = User.objects.create_superuser(email='admin@test.com', password="12345")
    client.force_authenticate(user=admin)

    category = ProductCategory.objects.create(name="category1", letter_code="ZZ")
    product1 = Product.objects.create(name="Product1", description="This is a great product!", price=13.99, category=category)
    product2 = Product.objects.create(name="Product2", description="This is a great product!", price=14.99, category=category)

    url = reverse('products:product-get-product-by-article', kwargs={'article_number': f'{product1.article_number}'})
    response = client.get(url)

    assert response.data['name'] == "Product1"

    payload = {
        'name': "Updated Product"
    }

    response = client.patch(url, payload)

    assert response.status_code == 200
    assert response.data['name'] == payload['name']