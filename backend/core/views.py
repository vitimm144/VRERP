from rest_framework import viewsets
from core.serializers import ClientSerializer
from core.models import Client


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
