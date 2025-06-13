import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User

@pytest.mark.django_db
def test_category_list_success():
    client = APIClient()

    admin = User.objects.create_superuser(email='admin@test.com', password="12345")
    client.force_authenticate(user=admin)

    url = reverse('carts:cart-list')
    response = client.get(url)
    
    assert response.status_code == 200
    