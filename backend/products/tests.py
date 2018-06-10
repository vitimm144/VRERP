from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from products.models import Product
from users.models import Employee, Career
from django.contrib.auth.models import User


class ProductTestCase(APITestCase):

    def setUp(self):
        # Setting user credentials. See fixtures files for more details.
        self.user = User.objects.create_superuser(
            username='admin', email='vs@vs.com', password='123'
        )
        self.client.force_authenticate(
            user=self.user,
            token=self.user.auth_token
        )

    def test_create_with_price(self):
        data = {
            "description": "Cebola",
            "code": "002",
            "size": "P",
            "amount": 10,
            "products": [
                {
                    "value": "20.00",
                },

            ],

        }
        response = self.client.post(
            reverse('product-list'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_price(self):
        data = {
            "description": "Cebola",
            "code": "002",
            "size": "P",
            "amount": 10,
            "products": [
                {
                    "value": "20.00",
                    "in_use": True
                },

            ],

        }
        response = self.client.post(
            reverse('product-list'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        value = response.data

        import ipdb; ipdb.set_trace()
        price = value.get('products')
        self.assertEqual(price[0].get('value'), "20.00")


class SaleTestCase(APITestCase):

    def setUp(self):
        # Setting user credentials. See fixtures files for more details.
        self.user = User.objects.create_superuser(
            username='admin', email='vs@vs.com', password='123'
        )
        self.client.force_authenticate(
            user=self.user,
            token=self.user.auth_token
        )

    def test_create(self):
        data = {
            "description": "Jaqueta de couro",
            "code": "006",
            "size": "P",
            "amount": 10,
            "products": [
                {
                    "value": "700.00",
                },

            ],

        }
        response = self.client.post(
            reverse('product-list'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        value = response.data

        career = Career.objects.create(
            title='Vendedora',
            description='Que vende'
        )

        employee = Employee.objects.create(
            name='Maria',
            cpf='12388933478',
            rg='76333552',
            address='Rua José Bonifacio',
            code='001',
            salary=1340.21,
            career=career
        )

        data = {
            "description": "Cebola",
            "products": [value],
            "payments": [
                {
                    "value": 200.00,
                    "mode": "A"
                },
                {
                    "value": 500.00,
                    "mode": "CP",
                    "plots_amount": 2,
                    "plots": [
                        {
                            "date": "21-01-18",
                            "plot": 1,
                            "ploted_value": 250.00
                        },
                        {
                            "date": "21-02-18",
                            "plot": 2,
                            "ploted_value": 250.00
                        }

                    ]
                }
            ],
            "saleswoman": employee.id,
            "status": "F",
            "deduction": 0.05

        }
        response = self.client.post(
            reverse('sales-list'),
            data
        )
        import ipdb;
        ipdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



