from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status
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
                },

            ],

        }
        response = self.client.post(
            reverse('product-list'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        value = response.data

        # import ipdb; ipdb.set_trace()
        price = value.get('products')
        self.assertEqual(price[0].get('value'), "20.00")

