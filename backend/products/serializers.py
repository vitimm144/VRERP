from django.conf.urls import url, include
from products.models import Product, ProductSale, ProductTrade
from products.models import Price, Pay, Plot, Stock, Color
from products.models import Sale
from django.db import transaction, IntegrityError
from rest_framework import routers, serializers, viewsets



class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = (
            'id',
            'created',
            'modified',
            'code',
            'name',
        )


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = (
            'id',
            'in_use',
            'value',
            'whole_sale_value',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
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
            'id',
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
            'price',
            'id',
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
            'price',
            'color',
        )

    def create(self, validated_data):
        return self.create_update(None, validated_data)

    def update(self, instance, validated_data):
        return self.create_update(instance, validated_data)

    def create_update(self, instance, validated_data):
        prices = validated_data.pop('products', [])

        if not instance:

            instance = super(ProductSerializer, self).create(validated_data)
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

        if prices:
            with transaction.atomic():
                ids = []
                for x in prices:
                    identifier = x.get('id')
                    if identifier:
                        ids.append(identifier)
                for price in instance.products.exclude(pk__in=ids):
                    price.set_in_use()

                for product in prices:
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
        read_only_fields = (
            'price',
        )
        fields = (
            'id',
            'product',
            'user',
            'amount',
            'price',
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
            'pay_sale',
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
                    try:
                        pl = instance.plots.get(plot=x.get('plot'))
                    except:
                        pl = None


                    if pl:
                        x['id'] = pl.id
                        ids.append(pl.id)
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


class ProductTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTrade
        fields = (
            'id',
            'product',
            'amount',
            'price',
        )


class ProductSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSale
        fields = (
            'id',
            'product',
            'amount',
            'price',
            'price_value',
            'enable_deduction'
        )
        read_only_fields = (
            'price_value',
            'price_whole_sale',
        )


class SaleSerializer(serializers.ModelSerializer):
    products = ProductSaleSerializer(many=True)
    products_trade = ProductTradeSerializer(many=True, required=False)
    payments = PaySerializer(many=True)

    class Meta:
        model = Sale
        read_only_fields = (
            'created',
            'modified',
            'total',
            'saleswoman_str',
            'user_str',
            'id',
        )
        fields = (
            'id',
            'products',
            'products_trade',
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
            'whole_sale',
        )
        # depth = 1

    def create(self, validated_data):
        return self.create_update(None, validated_data)

    def update(self, instance, validated_data):
        return self.create_update(instance, validated_data)

    def create_update(self, instance, validated_data):
        products = validated_data.pop('products', None)
        payments = validated_data.pop('payments', None)
        products_trade = validated_data.pop('products_trade', None)

        if not instance:
            instance = super(SaleSerializer, self).create(validated_data)
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

        if products:
            with transaction.atomic():
                ids = []

                for x in products:
                    try:
                        #recuperando o id removido pelo validated data.
                        prod_sale = instance.products.get(product=x.get('product'))
                    except:
                        prod_sale = None

                    if prod_sale:
                        x['id'] = prod_sale.id
                        ids.append(prod_sale.id)

                instance.products.exclude(id__in=ids).delete()

                for product in products:
                    if not product.get('id'):
                        product_product = product.get('product')
                        price = product.get('price')
                        amount = product.get('amount')

                        ProductSale.objects.create(
                            product_sale=instance,
                            product=product_product,
                            price=price,
                            amount=amount,
                            enable_deduction=product_product.enable_deduction
                        )
                    else:
                        edited_product = ProductSale.objects.get(pk=product.get('id'))
                        for attr, value in product.items():
                            setattr(edited_product, attr, value)
                            edited_product.save()

        if products_trade:
            with transaction.atomic():
                ids = []
                for x in products_trade:

                    try:
                        prod_trade = instance.products_trade.get(product=x.get('product'))
                    except:
                        prod_trade = None


                    if prod_trade:
                        x['id'] = prod_trade.id
                        ids.append(prod_trade.id)

                instance.products_trade.exclude(pk__in=ids).delete()

                for trade in products_trade:
                    if not trade.get('id'):
                        product_product = trade.get('product')
                        price = trade.get('price')
                        amount = trade.get('amount')

                        ProductTrade.objects.create(
                            sale=instance,
                            product=product_product,
                            price=price,
                            amount=amount,
                        )
                    else:
                        edited_product = ProductTrade.objects.get(pk=product.get('id'))
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
