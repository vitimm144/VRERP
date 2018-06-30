from rest_framework import viewsets
from users.serializers import UserSerializer
from products.serializers import ProductSerializer, SaleSerializer, StockSerializer
from products.models import Product, Sale, Stock
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']


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
