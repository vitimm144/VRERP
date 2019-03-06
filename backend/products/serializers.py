from django.conf.urls import url, include
from products.models import Product, ProductSale
from products.models import Price, Pay, Plot, Stock
from products.models import Sale
from django.db import transaction, IntegrityError
from rest_framework import routers, serializers, viewsets
from pprint import pprint
from django.db.models import Max

from users.serializers import UserSerializer


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = (
            'id',
            'in_use',
            'value',
            'created',
            'modified',
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
            'ploted_value',
            'created',
            'modified',
        )
        read_only_fields = (
            'created',
            'modified',
        )


class ProductSerializer(serializers.ModelSerializer):

    products = PriceSerializer(many=True)

    class Meta:
        model = Product
        read_only_fields = (
            'created',
            'modified',
            'amount',
        )
        fields = (
            'id',
            'products',
            'picture',
            'code',
            'description',
            'size',
            'amount',
            'enable_deduction',
            'created',
            'modified',
        )

    def create(self, validated_data):
        return self.create_update(None, validated_data)

    def update(self, instance, validated_data):
        return self.create_update(instance, validated_data)

    def create_update(self, instance, validated_data):
        # print()
        # pprint(validated_data)
        products = validated_data.pop('products', [])

        if not instance:

            instance = super(ProductSerializer, self).create(validated_data)
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
        # import ipdb; ipdb.set_trace()
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


class StockSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    # user = UserSerializer()

    class Meta:
        model = Stock
        fields = (
            'id',
            'product',
            'user',
            'amount'
        )
        depth = 1

    def to_internal_value(self, data):
        # Salvando objetos em atributos da classe para poder resgata-los
        # no metodo para salvar. Esse rack é necessário pois a validação do
        # serializar tira os objetos.
        self._produto = data.get('product')
        self._user = data.get('user')
        return super(StockSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        return self.create_update(None, validated_data)

    def update(self, instance, validated_data):
        return self.create_update(instance, validated_data)

    def create_update(self, instance, validated_data):
        # Rack para utilizar depth no serializer
        validated_data['product_id'] = self._produto.get('id')
        validated_data['user_id'] = self._user.get('id')

        if not instance:

            instance = super(StockSerializer, self).create(validated_data)
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

        instance.save()
        return instance


class PaySerializer(serializers.ModelSerializer):
    plots = PlotSerializer(many=True, required=False)

    class Meta:
        model = Pay
        fields = (
            'id',
            'plots',
            'value',
            'mode',
            'plots_amount',
            'created',
            'modified',
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
            instance = super(PaySerializer, self).create(validated_data)
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

        if plots:
            with transaction.atomic():
                # Treatment to delete campaign field.
                ids = []
                for x in plots:
                    identifier = x.get('id')
                    if identifier:
                        ids.append(identifier)
                instance.plots.exclude(pk__in=ids).delete()

                for plot in plots:
                    if not plot.get('id'):
                        Plot.objects.create(
                            plot_pay=instance,
                            **plot
                        )
                    else:
                        edited_plot = Price.objects.get(pk=plot.get('id'))
                        for attr, value in plot.items():
                            setattr(edited_plot, attr, value)
                            edited_plot.save()

        instance.save()

        return instance


class ProductSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSale
        fields = (
            'id',
            'product',
            'amount',
            'price'
        )


class SaleSerializer(serializers.ModelSerializer):
    products = ProductSaleSerializer(many=True)
    payments = PaySerializer(many=True)

    class Meta:
        model = Sale
        read_only_fields = (
            'created',
            'modified',
            'total',
            'saleswoman_str',
            'user_str',
        )
        fields = (
            'id',
            'products',
            'payments',
            'status',
            'saleswoman',
            'client',
            'deduction',
            'user',
            'total',
            'saleswoman_str',
            'user_str',
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

        pprint(validated_data)
        if not instance:
            instance = super(SaleSerializer, self).create(validated_data)
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

        if products:
            with transaction.atomic():
                ids = []
                for x in products:
                    identifier = x.get('id')
                    if identifier:
                        ids.append(identifier)
                instance.products.exclude(pk__in=ids).delete()

                for product in products:
                    if not product.get('id'):
                        ProductSale.objects.create(
                            product_sale=instance,
                            **product
                        )
                    else:
                        edited_product = ProductSale.objects.get(pk=product.get('id'))
                        for attr, value in product.items():
                            setattr(edited_product, attr, value)
                            edited_product.save()

        if payments:
            with transaction.atomic():
                ids = []
                for x in payments:
                    identifier = x.get('id')
                    if identifier:
                        ids.append(identifier)
                # import ipdb; ipdb.set_trace()
                instance.payments.exclude(pk__in=ids).delete()

                for pay in payments:
                    if not pay.get('id'):
                        pay['pay_sale'] = instance
                        serialized_pay = PaySerializer(data=pay)
                        serialized_pay.is_valid()
                        serialized_pay.create(validated_data=serialized_pay.validate(pay))

                    else:
                        edited_pay = Pay.objects.get(pk=pay.get('id'))
                        for attr, value in pay.items():
                            setattr(edited_pay, attr, value)
                            edited_pay.save()

        instance.save()

        return instance
