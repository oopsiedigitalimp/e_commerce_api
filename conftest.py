import pytest
from products.models import Product, ProductCategory

@pytest.fixture(autouse=True)
def clear_products():
    Product.objects.all().delete()

@pytest.fixture(autouse=True)
def clear_categories():
    ProductCategory.objects.all().delete()