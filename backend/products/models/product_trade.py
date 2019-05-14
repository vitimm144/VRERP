from django.db import models


class ProductTrade(models.Model):
    product = models.ForeignKey(
        "Product",
        verbose_name="Produto",
        related_name="product_trade",
        on_delete=models.DO_NOTHING
    )
    price = models.ForeignKey(
        "Price",
        verbose_name="Preço",
        related_name="price_trade",
        on_delete=models.DO_NOTHING
    )
    amount = models.IntegerField(
        verbose_name='Quantidade',
        default=1
    )
    sale = models.ForeignKey("Sale", related_name='products_trade', default=None, on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.product.description

    class Meta:
        ordering = ["id"]