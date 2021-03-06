from rest_framework import viewsets

from products.serializers import ProductSerializer, SaleSerializer, StockSerializer, ColorSerializer, \
    StockOperationSerializer
from products.serializers import ProductOperationSerializer
from products.models import Product, Sale, Stock, Color, ProductOperation, StockOperation

from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from pprint import pprint

import django_filters.rest_framework


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch', 'delete']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('created', 'code', 'name',)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch', 'delete']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('created', 'code', 'size',)


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch', 'delete']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('status', 'client', 'saleswoman', 'user', 'user__username')
    search_fields = ('created',)


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch', 'delete']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('product', 'user', 'user__username')

class ProductOperationViewSet(viewsets.ModelViewSet):
    queryset = ProductOperation.objects.all()
    serializer_class = ProductOperationSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch', 'delete']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('product', 'store', 'store__username', 'type', 'reason')

class StockOperationViewSet(viewsets.ModelViewSet):
    queryset = StockOperation.objects.all()
    serializer_class = StockOperationSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch', 'delete']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('product_operation', 'stock' )

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
        store = request.data.get('user')
        amount = request.data.get('amount')
        store_from = stock.get('user')
        try:
            with transaction.atomic():
                #verificar se existe o produto no estoque do usuario a ser transferido
                ProductOperation.objects.create(
                    reason='TF',
                    type='E',
                    store_id=store,
                    product_id=product.get('id'),
                    amount=amount
                )

                ProductOperation.objects.create(
                    reason='TF',
                    type='S',
                    store_id=store_from.get('id'),
                    product_id=product.get('id'),
                    amount=amount
                )

        except Exception as e:
            content = {'success': False, 'message': e}
            print(e)
            return Response(status=400, data=content)

        content = {'success': True}
        return Response(status=200, data=content)


class SaleTradeView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None, *args, **kwargs):
        content = dict()
        sale = request.data.get('sale')
        traded = request.data.get('traded')


        try:
            with transaction.atomic():
                sale_instance = Sale.objects.get(id=sale.get('id'))
                sale['products_trade'] = traded
                serialized_sale = SaleSerializer(data=sale)
                serialized_sale.is_valid()
                validated_data = serialized_sale.validated_data
                serialized_sale.update(sale_instance, validated_data)

                if traded:
                    for trade in traded:
                        amount = trade.get('amount')
                        #Devolvendo o produto trocado ao estoque.
                        stock_to_filter = Stock.objects.filter(product_id=trade.get('product'), user_id=sale.get('user'))
                        if len(stock_to_filter) == 0:
                            stock_to = Stock.objects.create(
                                product__id=trade.get('product'),
                                user__id=sale.get('user'),
                                amount=trade.get('amount')
                             )
                        else:
                            stock_to = stock_to_filter[0]
                            stock_to.amount += amount
                            stock_to.save()

        except Exception as e:
            content = {'success': False, 'message': 'Error while trading'}
            return Response(status=400, data=content)

        # import ipdb; ipdb.set_trace()

        content = {'success': True}
        return Response(status=200, data=content)