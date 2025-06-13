import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from products.models import Product, ProductCategory

@pytest.mark.django_db
def test_category_list_success():
    client = APIClient()

    admin = User.objects.create_user(email='admin@test.com', password="12345", role='Admin')
    client.force_authenticate(user=admin)

    ProductCategory.objects.create(name="category1", letter_code="ZZA")
    ProductCategory.objects.create(name="category2", letter_code="ZZB")

    url = reverse('products:categories:category-list')
    print(url)
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data['count'] == 2
    