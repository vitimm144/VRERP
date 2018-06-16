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
        
    def __str__(self):
        return self.product.code
