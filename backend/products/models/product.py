from django.db import models


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
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    enable_deduction = models.BooleanField('Habilitar desconto', default=True)

    @property
    def amount(self):
        amount = self.stock_set.all().aggregate(models.Sum('amount'))
        return amount.get("amount__sum") or 0

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.code
