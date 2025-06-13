import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from products.models import Product, ProductCategory

@pytest.mark.django_db
def test_create_category_unauthorized():
    client = APIClient()

    payload = {
        'name': "Category1",
        'letter_code': "ZZ"
    }

    url = reverse('products:categories:category-list')
    response = client.post(url, payload)

    assert response.status_code == 401