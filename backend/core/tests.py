from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from products.models import Product, Sale, Stock, Price, Color
from users.models import Employee, Career
from django.contrib.auth.models import User
from core.models import Client


class ClientTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin', email='vs@vs.com', password='123'
        )
        self.client.force_authenticate(
            user=self.user,
            token=self.user.auth_token
        )

    def test_create_client(self):
        data={
            "name": "Victor",
            "cpf": "122333444",
            "rg": "543563464",
            "address":"Rua jose das coves",
            "cep": "456546",
            "phone":"55667788657",
            "email": "victor@mail.com"
        }
        url = reverse('client-list')
        response = self.client.post(
            url,
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_client(self):
        data={
            "name": "Victor",
            "cpf": "122333444",
            "rg": "543563464",
            "address":"Rua jose das coves",
            "cep": "456546",
            "phone":"55667788657",
            "email": "victor@mail.com"
        }
        url = reverse('client-list')
        response = self.client.post(
            url,
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        client = response.data
        pk = client.get('id')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(
            reverse('client-detail', kwargs={'pk': pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)