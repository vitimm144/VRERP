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
    code = models.CharField(verbose_name="Código", max_length=255)
    description = models.TextField(null=True, blank=True, verbose_name="Descrição")
    size = models.CharField(choices=SIZE, verbose_name="Tamanho", max_length=3)
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    enable_deduction = models.BooleanField('Habilitar desconto', default=False)
    color = models.ForeignKey(
        'Color',
        verbose_name="Cor",
        on_delete=models.DO_NOTHING,
    )

    @property
    def amount(self):
        amount = self.stock_set.all().aggregate(models.Sum('amount'))
        return amount.get("amount__sum") or 0

    @property
    def price(self):
        price = self.products.get()
        return price.value or 0.00

    class Meta:

        ordering = ["id", "code"]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        unique_together = ['code', 'size', 'color']
        indexes = [
            models.Index(fields=['code', 'size', 'color']),
        ]

    def __str__(self):
        return self.code
