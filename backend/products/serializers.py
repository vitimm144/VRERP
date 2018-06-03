from django.conf.urls import url, include
from products.models import Product, ProductSale
from products.models import Price, Pay, Plot
from products.models import Sale
from django.db import transaction, IntegrityError
from rest_framework import routers, serializers, viewsets


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = (
            'id',
            'in_use',
            'value'
        )
        read_only_fields = (
            'created',
            'modified',
        )


class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = (
            'id',
            'date',
            'plot',
            'ploted_value'
        )
        read_only_fields = (
            'created',
            'modified',
        )


class ProductSerializer(serializers.ModelSerializer):

    products = PriceSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'products',
            'picture',
            'code',
            'description',
            'size',
            'amount',
        )
        read_only_fields = (
            'created',
            'modified',
        )

    def create(self, validated_data):
        return self.create_update(None, validated_data)

    def update(self, instance, validated_data):
        return self.create_update(instance, validated_data)

    def create_update(self, instance, validated_data):

        products = validated_data.pop('products', [])

        if not instance:

            instance = super(ProductSerializer, self).create(validated_data)
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

        if products:
            with transaction.atomic():
                # Treatment to delete campaign field.
                ids = []
                for x in products:
                    identifier = x.get('id')
                    if identifier:
                        ids.append(identifier)
                for price in instance.products.exclude(pk__in=ids):
                    price.set_in_use()

                for product in products:
                    if not product.get('id'):
                        Price.objects.create(
                            product=instance,
                            **product
                        )
                    else:
                        edited_product = Price.objects.get(pk=product.get('id'))
                        for attr, value in product.items():
                            setattr(edited_product, attr, value)
                            edited_product.save()

        instance.save()

        return instance


class PaySerializer(serializers.ModelSerializer):
    plots = serializers.PrimaryKeyRelatedField(
        required=True,
        many=True,
        queryset=Plot.objects.all()
    )

    class Meta:
        model = Sale
        fields = (
            'id',
            'plots',
            'value',
            'mode',
            'plots_amount'
        )
        read_only_fields = (
            'created',
            'modified',
        )

    def create(self, validated_data):
        return self.create_update(None, validated_data)

    def update(self, instance, validated_data):
        return self.create_update(instance, validated_data)

    def create_update(self, instance, validated_data):
        plots = validated_data.pop('plots', None)

        if not instance:
            instance = super(PlotSerializer, self).create(validated_data)
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

        if plots is not None:
            if instance.products.count():
                instance.plots.remove(*instance.plots.all())
            instance.products.add(*plots)

        instance.save()

        return instance


class ProductSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSale
        fields = (
            'id',
            'product',
            'price'
        )


class SaleSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        required=True,
        many=True,
        queryset=ProductSale.objects.all()
    )
    payments = serializers.PrimaryKeyRelatedField(
        required=True,
        many=True,
        queryset=Pay.objects.all()
    )

    class Meta:
        model = Sale
        fields = (
            'id',
            'products',
            'payments',
            'status',
            'saleswoman',
            'client',
            'deduction'
        )
        read_only_fields = (
            'created',
            'modified',
        )

    def create(self, validated_data):
        return self.create_update(None, validated_data)

    def update(self, instance, validated_data):
        return self.create_update(instance, validated_data)

    def create_update(self, instance, validated_data):
        products = validated_data.pop('products', None)
        payments = validated_data.pop('payments', None)

        if not instance:
            instance = super(SaleSerializer, self).create(validated_data)
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

        if products is not None:
            if instance.products.count():
                instance.products.remove(*instance.products.all())

            instance.products.add(*products)

        if payments is not None:
            if instance.payments.count():
                instance.payments.remove(*instance.payments.all())
            instance.payments.add(*payments)

        instance.save()

        return instance