import pytest
from rest_framework.test import APIClient
from users.models import User
from products.models import Product, ProductCategory

@pytest.mark.django_db
def test_product_update_by_article_number_success():
    client = APIClient()

    admin = User.objects.create_user(email='admin@test.com', password="12345", role='Admin')
    client.force_authenticate(user=admin)

    category = ProductCategory.objects.create(name="category1", letter_code="ZZ")
    product1 = Product.objects.create(name="Product1", description="This is a great product!", price=13.99, category=category)
    product2 = Product.objects.create(name="Product2", description="This is a great product!", price=14.99, category=category)

    response = client.get(f"/products/{product1.id}/")

    assert response.data['name'] == "Product1"

    data = {
        'name': "Updated Product"
    }

    response = client.patch(f"/products/{product1.id}/", data)

    assert response.data['name'] == "Updated Product"