from rest_framework import viewsets
from core.serializers import ClientSerializer
from core.models import Client
import django_filters.rest_framework


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('name', 'email', 'cpf', 'rg', 'employee',)
