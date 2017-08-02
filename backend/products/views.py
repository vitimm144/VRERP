from rest_framework import viewsets
from users.serializers import UserSerializer
from products.serializers import ProductSerializer
from products.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
