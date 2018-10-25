from rest_framework import viewsets
from users.serializers import UserSerializer
from products.serializers import ProductSerializer, SaleSerializer, StockSerializer
from products.models import Product, Sale, Stock
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
import django_filters.rest_framework


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class AvailabilityView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        amount = int(request.query_params.get('amount'))
        product_id = request.query_params.get('product_id')
        user_id = request.query_params.get('user_id')
        try:
            stock = Stock.objects.filter(product__id=product_id, user__id=user_id)[0]
        except IndexError:
            return Response(status=400)

        if stock.amount <= amount:
            content = {'available': True}
        else:
            content = {'available': False}
        return Response(content)


class StockTransferView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None, *args, **kwargs):
        content = dict()
        stock = request.data.get('stock')
        product = stock.get('product')
        sale = request.data.get('user')
        amount = request.data.get('amount')
        try:
            with transaction.atomic():
                #verificar se existe o produto no estoque do usuario a ser transferido
                stock_to_filter = Stock.objects.filter(product__id=product.get('id'), user__id=sale)
                # import ipdb; ipdb.set_trace()
                if len(stock_to_filter) == 0:
                    stock_to = Stock.objects.create(product_id=product.get('id'), user_id=sale, amount=amount)
                else:
                    stock_to = stock_to_filter[0]
                    stock_to.amount += amount
                    stock_to.save()

                #decrementando o stock do produto
                stock_from = Stock.objects.get(id=stock.get('id'))
                stock_from.amount -= amount
                stock_from.save()
        except Exception as e:
            content = {'success': False, 'message': e}
            print(e)
            return Response(status=400, data=content)

        # import ipdb; ipdb.set_trace()

        content = {'success': True}
        return Response(status=200, data=content)


