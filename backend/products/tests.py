from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from products.models import Product, Sale, Stock
from users.models import Employee, Career
from django.contrib.auth.models import User


class ProductTestCase(APITestCase):

    def setUp(self):
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
            "products": [
                {
                    "value": "20.00",
                }

            ],

        }
        url = reverse('product-list')

        response = self.client.post(
            url,
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_price(self):
        data = {
            "description": "Cebola",
            "code": "002",
            "size": "P",
            "products": [
                {
                    "value": "20.00",
                    "in_use": True
                },

            ],

        }
        url = reverse('product-list')
        response = self.client.post(
            url,
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        value = response.data

        # import ipdb; ipdb.set_trace()
        price = value.get('products')
        self.assertEqual(price[0].get('value'), "20.00")


class SaleTestCase(APITestCase):
    user = {}
    carrer = dict()
    employee = dict()

    def setUp(self):
        # Setting user credentials. See fixtures files for more details.
        self.user = User.objects.create_superuser(
            username='admin', email='vs@vs.com', password='123'
        )
        self.client.force_authenticate(
            user=self.user,
            token=self.user.auth_token
        )

        self.career = Career.objects.create(
            title='Vendedora',
            description='Que vende'
        )

        self.employee = Employee.objects.create(
            name='Maria',
            cpf='12388933478',
            rg='76333552',
            address='Rua José Bonifacio',
            code='001',
            salary=1340.21,
            career=self.career
        )
        data = {
            "description": "Jaqueta de couro",
            "code": "006",
            "size": "P",
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

        data = {
            "description": "Jeans",
            "code": "007",
            "enable_deduction": True,
            "size": "P",
            "products": [
                {
                    "value": "120.00",
                },

            ],

        }

        response = self.client.post(
            reverse('product-list'),
            data
        )


    def test_create(self):

        response = self.client.get(reverse('product-list'))
        json_response = response.json()
        products = []
        for prod in json_response.get('results'):
            products.append(
                {
                    "product": prod.get("id"),
                    "amount": 1,
                    "price": prod.get("products")[0].get("id")
                }
            )

        self.assertEqual(len(products), 2)
        data = {
            "products": products,
            "payments": [
                {
                    "value": 320.00,
                    "mode": "A"
                },
                {
                    "value": 500.00,
                    "mode": "CP",
                    "plots_amount": 2,
                    "plots": [
                        {
                            "date": "2018-01-21 00:00:00",
                            "plot": 1,
                            "ploted_value": 250.00
                        },
                        {
                            "date": "2018-02-21 00:00:00",
                            "plot": 2,
                            "ploted_value": 250.00
                        }

                    ]
                }
            ],
            "saleswoman": self.employee.id,
            "user": self.user.id,
            "status": "F",
            "deduction": 0.05
        }
        response = self.client.post(
            reverse('sale-list'),
            data
        )
        # import ipdb; ipdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_trade(self):
        data = {
            "description": "Casaco de couro",
            "code": "008",
            "size": "M",
            "amount": 10,
            "products": [
                {
                    "value": "750.00",
                },

            ],

        }
        response = self.client.post(
            reverse('product-list'),
            data
        )
        # Criando stoque para os produtos
        for prod in Product.objects.all():
            Stock.objects.create(
                user=self.user,
                product=prod,
                amount=10
            )

        self.assertEqual(len(Stock.objects.all()), 3)

        response = self.client.get(reverse('product-list'))
        json_response = response.json()
        products = []
        for prod in json_response.get('results'):
            products.append(
                {
                    "product": prod.get("id"),
                    "amount": 1,
                    "price": prod.get("products")[0].get("id")
                }
            )

        self.assertEqual(len(products), 3)
        data = {
            "products": products,
            "payments": [
                {
                    "value": 320.00,
                    "mode": "A"
                },
                {
                    "value": 1000.00,
                    "mode": "CP",
                    "plots_amount": 2,
                    "plots": [
                        {
                            "date": "2019-01-21 00:00:00",
                            "plot": 1,
                            "ploted_value": 250.00
                        },
                        {
                            "date": "2019-02-21 00:00:00",
                            "plot": 2,
                            "ploted_value": 750.00
                        }

                    ]
                }
            ],
            "saleswoman": self.employee.id,
            "user": self.user.id,
            "status": "F",
            "deduction": 0.05
        }
        response = self.client.post(
            reverse('sale-list'),
            data
        )
        # import ipdb; ipdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "description": "Camisa Polo",
            "code": "010",
            "enable_deduction": True,
            "size": "P",
            "amount": 10,
            "products": [
                {
                    "value": "120.00",
                },

            ],

        }

        response = self.client.post(
            reverse('product-list'),
            data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_product = response.json()
        #Criando stoque para o novo produto
        Stock.objects.create(
            user=self.user,
            product_id=new_product.get("id"),
            amount=10
        )
        self.assertEqual(len(Stock.objects.all()), 4)

        response = self.client.get(
            reverse('sale-list'),
            data
        )
        json_response = response.json()

        sale = json_response.get('results')[0]
        self.assertEqual(len(sale.get('products')), 3)


        product_to_trade = sale['products'].pop()

        sale['products'].append(
            {
                "product": new_product.get("id"),
                "amount": 1,
                "price": new_product.get("products")[0].get("id")
            }
        )
        #
        data = {
            "sale": sale,
            "traded": [ product_to_trade, ]
        }



        response = self.client.post(
            reverse('sale_trade'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sales = Sale.objects.all()
        self.assertEqual(len(sales), 1)
        sale = sales[0]
        products = sale.products.all()
        self.assertEqual(len(products), 3)
        traded = sale.products_trade.all()
        self.assertEqual(len(traded), 1)
        import ipdb; ipdb.set_trace()






