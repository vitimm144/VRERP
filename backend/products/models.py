from django.db import models


class PriceManager(models.Manager):
    def get_queryset(self):
        return super(PriceManager, self).get_queryset().filter(in_use=True)


class Product(models.Model):
    SIZE = (
        ('PP', 'PP'),
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
        ('GG', 'GG'),
    )
    picture = models.ImageField(null=True, verbose_name="Foto", upload_to='products/')
    code = models.CharField(unique=True, verbose_name="Código", max_length=255)
    description = models.TextField(null=True, blank=True, verbose_name="Descrição")
    size = models.CharField(choices=SIZE, verbose_name="Tamanho", max_length=3)
    amount = models.IntegerField(verbose_name="Quantidade")
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.code


class Price(models.Model):
    objects = PriceManager()
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    in_use = models.BooleanField(default=True, verbose_name="Em uso")
    value = models.DecimalField(decimal_places=2, max_digits=7, verbose_name="Valor")
    product = models.ForeignKey(
        "Product",
        verbose_name="Produto",
        related_name="products",
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return str(self.value)

    def delete(self, using=None):
        self.in_use = False
        self.save()

    def set_in_use(self):
        self.in_use = False
        self.save()

    class Meta:
        ordering = ["value"]


PAY_MODE = (
        ('D', 'DÉBITO'),
        ('CA', 'CRÉDITO À VISTA'),
        ('CP', 'CRÉDITO PARCELADO'),
        ('A', 'À VISTA'),
        ('CHA', 'CHEQUE À VISTA'),
        ('CHP', 'CHEQUE PARCELADO'),
        ('VP', 'VALE PARCELADO'),
        ('V', 'VALE'),

    )


class Plot(models.Model):
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    date = models.DateTimeField('Data')
    plot = models.IntegerField(verbose_name='Parcela')
    ploted_value = models.DecimalField(
        decimal_places=2,
        max_digits=7,
        verbose_name="Valor da parcela"
    )


class Pay(models.Model):
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=7, verbose_name="Valor")
    mode = models.CharField(choices=PAY_MODE, verbose_name="Modo", max_length=3)
    plots_amount = models.IntegerField(
        verbose_name='Número de parcelas',
        null=True,
        blank=True
    )
    plots = models.ManyToManyField(
        'Plot',
        related_name='plots',
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.value)

    class Meta:
        ordering = ["value"]


class ProductSale(models.Model):
    product = models.ForeignKey(
        "Product",
        verbose_name="Produto",
        related_name="product_sale",
        on_delete=models.DO_NOTHING
    )
    price = models.ForeignKey(
        "Price",
        verbose_name="Produto",
        related_name="price_sale",
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        self.product.description


class Sale(models.Model):

    STATUS = (
        ('C', 'CANCELADA'),
        ('F', 'FINALIZADA'),

    )

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    products = models.ManyToManyField("ProductSale", related_name='products')
    payments = models.ManyToManyField("Pay", related_name='payments')
    saleswoman = models.ForeignKey(
        "users.Employee",
        related_name='employee',
        on_delete=models.DO_NOTHING,
        verbose_name="Vendedora"
    )
    status = models.CharField(choices=STATUS, verbose_name="Status", max_length=3)
    deduction = models.DecimalField(
        verbose_name="Desconto",
        null=True,
        blank=True,
        max_digits=7,
        decimal_places=3
    )
    client = models.ForeignKey(
        "core.Client",
        verbose_name="Cliente",
        null=True,
        blank=True,
        related_name="client",
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.status

    class Meta:
        ordering = ['created', 'status']
