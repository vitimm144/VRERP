from django.db import models


class ProductTrade(models.Model):
    product = models.ForeignKey(
        "Product",
        verbose_name="Produto",
        related_name="product_trade",
        null=True,
        on_delete=models.SET_NULL
    )
    price = models.ForeignKey(
        "Price",
        verbose_name="Preço",
        related_name="price_trade",
        null=True,
        on_delete=models.SET_NULL
    )
    amount = models.IntegerField(
        verbose_name='Quantidade',
        default=1
    )
    sale = models.ForeignKey(
        "Sale",
        related_name='products_trade',
        default=None,
        null=True,
        on_delete=models.SET_NULL
    )


    def __str__(self):
        return self.product.description

    class Meta:
        ordering = ["id"]