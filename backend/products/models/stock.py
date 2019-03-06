from django.db import models
from django.conf import settings


class Stock(models.Model):
    product = models.ForeignKey("Product", verbose_name="Produto")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Loja")
    amount = models.IntegerField(
        verbose_name='Quantidade'
    )

    class Meta:
        unique_together = (("product", "user"),)

    @property
    def price(self):
        return self.product.price or 0.00

    def __str__(self):
        return self.product.code
