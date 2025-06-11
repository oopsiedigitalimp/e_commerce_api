import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from products.models import Product, ProductCategory

@pytest.mark.django_db
def test_create_category_success():
    client = APIClient()

    admin = User.objects.create_user(email='admin@test.com', password='12345', role='Admin')
    client.force_authenticate(user=admin)

    payload = {
        'name': "Category1",
        'letter_code': "ZZ"
    }
    url = reverse('products:category-list')
    response = client.post(url, payload, format='json')

    assert response.status_code == 201

    assert response.headers['Content-Type'] == 'application/json'

    data = response.json()
    assert data['name'] == payload['name']
    assert data['letter_code'] == payload['letter_code']

    assert ProductCategory.objects.filter(name="Category1").exists()