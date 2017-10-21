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


