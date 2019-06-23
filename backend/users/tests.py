from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from products.models import Product, Sale, Stock, Price, Color
from users.models import Employee, Career
from django.contrib.auth.models import User
from core.models import Client


class UsersTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin', email='vs@vs.com', password='123'
        )
        self.client.force_authenticate(
            user=self.user,
            token=self.user.auth_token
        )

    def test_create(self):
        data={
            "username": "Fabrica",
            "password": "123456",
            "is_staff": True,
            "is_active": True,
            "email": "fabrica@mail.com"
        }
        url = reverse('user-list')
        response = self.client.post(
            url,
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class EmployeeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin', email='vs@vs.com', password='123'
        )
        self.client.force_authenticate(
            user=self.user,
            token=self.user.auth_token
        )

    def test_create(self):
        career = Career.objects.create(
            title="Vendedor",
            description="Efetua vendas"
        )
        self.assertTrue(career.pk)
        data={
            "name": "Victor",
            "cpf": "123456",
            "rg": "234534",
            "salary": 700.00,
            "address": "Rua jose das coves",
            "email": "victor@mail.com",
            "code": "001",
            "career": career.pk,
            "birthday": "1986-05-14",
            "work_permit": "234532"

        }
        url = reverse('employee-list')
        response = self.client.post(
            url,
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)