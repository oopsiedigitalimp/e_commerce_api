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
    product = Product.objects.create(name="Product1", description="This is a great product!", price=13.99, category=category)

    response = client.get(f"/products/{product.id}/")

    assert response.status_code == 200

    response = client.delete(f"/products/{product.id}/")

    assert response.status_code == 204

    assert Product.objects.filter(id=product.id).count() == 0