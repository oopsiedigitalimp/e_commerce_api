import pytest
from rest_framework.test import APIClient
from users.models import User
from products.models import Product, ProductCategory

@pytest.mark.django_db
def test_product_list_filters_success():
    client = APIClient()

    admin = User.objects.create_user(email='admin@test.com', password="12345", role='Admin')
    client.force_authenticate(user=admin)

    category1 = ProductCategory.objects.create(name="category1", letter_code="ZZA")
    category2 = ProductCategory.objects.create(name="category2", letter_code="ZZB")
    category3 = ProductCategory.objects.create(name="category3", letter_code="ZZC")
    category4 = ProductCategory.objects.create(name="category4", letter_code="ZZD")

    Product.objects.create(name='Product1', description="It is a great product!", price=1.99, category=category1, stock=1)
    Product.objects.create(name='Product2', description="It is a great product!", price=2.99, category=category2)
    Product.objects.create(name='Product3', description="It is a great product!", price=3.99, category=category3)
    Product.objects.create(name='Product4', description="It is a great product!", price=4.99, category=category4)

    response = client.get("/products/?price_min=4")
    
    assert response.status_code == 200
    assert response.data['count'] == 1
    
    response = client.get("/products/?price_max=2")
    
    assert response.status_code == 200
    assert response.data['count'] == 1
    
    response = client.get(f"/products/?category={category1}")
    
    assert response.status_code == 200
    assert response.data['count'] == 1

    response = client.get(f"/products/?in_stock=true")
    
    assert response.status_code == 200
    assert response.data['count'] == 1 