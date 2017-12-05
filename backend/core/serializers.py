from django.conf.urls import url, include
from products.models import Product
from products.models import Price
from django.db import transaction, IntegrityError
from rest_framework import routers, serializers, viewsets


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = (
            'name',
            'cpf',
            'rg',
            'address',
            'cellphone',
            'phone',

        )
        read_only_fields = (
            'created',
            'modified',
        )
