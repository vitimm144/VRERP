from django.db import models
from django.conf import settings


class Stock(models.Model):
    product = models.ForeignKey("Product", verbose_name="Produto", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Loja", on_delete=models.DO_NOTHING)
    amount = models.IntegerField(
        verbose_name='Quantidade'
    )

    class Meta:
        ordering = ["id"]
        unique_together = (("product", "user"),)

    @property
    def price(self):
        return self.product.price or 0.00

    def __str__(self):
        return self.product.code
