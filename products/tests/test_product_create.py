import pytest
from rest_framework.test import APIClient
from users.models import User
from products.models import Product, ProductCategory

@pytest.mark.django_db
def test_create_product_success():
    client = APIClient()

    admin = User.objects.create_user(email='admin@test.com', password="12345", role='Admin')
    client.force_authenticate(user=admin)

    category = ProductCategory.objects.create(name="category1", letter_code="ZZ")

    payload = {
        "name": "Product1",
        "description": "This is a great product!",
        "price": 13.99,
        "category_id": category.id
    }

    response = client.post("/products/", payload, format='json')
    
    assert response.status_code == 201

    assert response.headers['Content-Type'] == 'application/json'

    data = response.json()
    assert data['name'] == payload['name']
    assert data['description'] == payload['description']
    assert float(data['price']) == payload['price']
    assert data['category'] == category.name
    assert data['stock'] == 0

    expected_article_number = f"{category.get_full_letter_code()}-0"
    assert data['article_number'] == expected_article_number

    assert Product.objects.filter(name="Product1").exists()