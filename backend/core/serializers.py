from django.conf.urls import url, include
from products.models import Product
from core.models import Client
from django.db import transaction, IntegrityError
from rest_framework import routers, serializers, viewsets


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'cpf',
            'rg',
            'address',
            'cellphone',
            'phone',
            'employee',
            'email',
            'facebook',
            'created',
            'modified',
        )
        read_only_fields = (
            'created',
            'modified',
        )
