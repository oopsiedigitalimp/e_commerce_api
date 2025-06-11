import pytest
from django.urls import reverse
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

    url = reverse('products:items:get_product_by_article_number', kwargs={'article_number': f'{product.id}'})
    response = client.get(url)

    assert response.status_code == 200

    response = client.delete(url)

    assert response.status_code == 204

    assert Product.objects.filter(id=product.id).count() == 0