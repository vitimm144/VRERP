from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from products.models import Product, Sale, Stock, Price, Color
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
        self.color = Color.objects.create(code='00', name='neutra')

    def test_create(self):
        color = Color.objects.create(code='01' , name='vermelho')
        self.assertTrue(color.pk)
        data = {
            "description": "Abacaxi",
            "code": "003",
            "size": "M",
            "color": color.pk,
            "products": [
                {
                    "value": "10.00",
                }

            ],

        }
        url = reverse('product-list')
        response = self.client.post(
            url,
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_with_price(self):
        data = {
            "description": "Cebola",
            "code": "002",
            "size": "P",
            "color": self.color.pk,
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
            "color": self.color.pk,
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


class StockTestCase(APITestCase):
    user = dict()
    product= dict()
    price= dict()
    def setUp(self):
        # Setting user credentials. See fixtures files for more details.
        self.user = User.objects.create_superuser(
            username='admin', email='vs@vs.com', password='123'
        )
        self.client.force_authenticate(
            user=self.user,
            token=self.user.auth_token
        )

        self.color = Color.objects.create(code='00', name='neutra')

        self.product = Product.objects.create(
            code="001",
            description='Tenis',
            color=self.color,
            size='P'

        )
        # self.price = Price.objects.create(
        #     value=200.00,
        #     product=self.product
        # )


    def test_create(self):
        stock = Stock.objects.create(
            product=self.product,
            user=self.user,
            amount=10
        )
        self.assertTrue(stock.pk)



class SaleTestCase(APITestCase):
    user = {}
    career = dict()
    employee = dict()
    color = None

    def setUp(self):
        # Setting user credentials. See fixtures files for more details.
        self.user = User.objects.create_superuser(
            username='admin', email='vs@vs.com', password='123'
        )

        self.client.force_authenticate(
            user=self.user,
            token=self.user.auth_token
        )

        self.color = Color.objects.create(code='00', name='neutra')

        self.career = Career.objects.create(
            title='Vendedora',
            description='Que vende'
        )

        data = {
            "description": "Jaqueta de couro",
            "code": "006",
            "color": self.color.pk,
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
            "color": self.color.pk,
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

        self.employee = Employee.objects.create(
            name='Maria',
            cpf='12388933478',
            rg='76333552',
            address='Rua José Bonifacio',
            code='001',
            salary=1340.21,
            career=self.career
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
        # import ipdb; ipdb.set_trace()
        response = self.client.post(
            reverse('sale-list'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sale = response.json()
        # import ipdb; ipdb.set_trace()
        self.assertEqual(len(sale.get('payments')), 2)
        payment = sale.get('payments')[1]
        self.assertEqual(len(payment.get('plots')), 2)


    def test_trade(self):
        data = {
            "description": "Casaco de couro",
            "code": "008",
            "color": self.color.pk,
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
        ##################################################################
        # Criando a venda para poder realizar a troca
        ##################################################################
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
        ##################################################################
        ##################################################################

        ##################################################################
        # Criando novo prouto para poder fazer a troca
        ##################################################################
        data = {
            "description": "Camisa Polo",
            "code": "010",
            "color": self.color.pk,
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
        ##################################################################

        response = self.client.get(
            reverse('sale-list'),
            data
        )
        json_response = response.json()

        sale = json_response.get('results')[0]
        self.assertEqual(len(sale.get('products')), 3)

        # import ipdb; ipdb.set_trace()
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

        for product in products:
            self.assertEqual(product.product.amount, 9)

        products = Product.objects.all()
        self.assertEqual(len(products), 4)

        self.assertEqual(products[2].amount, 10)

    def test_abc(self):
        self.assertTrue(True)








