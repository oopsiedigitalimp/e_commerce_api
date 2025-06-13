import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from carts.models import Cart

@pytest.mark.django_db
def test_cart_retrieve_success():
    client = APIClient()

    admin = User.objects.create_superuser(email='admin@test.com', password="12345")
    client.force_authenticate(user=admin)

    url = reverse('carts:cart-detail')
    response = client.get(url)

    assert response.status_code == 200