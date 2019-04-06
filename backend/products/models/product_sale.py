from django.db import models


class ProductSale(models.Model):
    product = models.ForeignKey(
        "Product",
        verbose_name="Produto",
        related_name="product_sale",
        on_delete=models.DO_NOTHING
    )
    price = models.ForeignKey(
        "Price",
        verbose_name="Preço",
        related_name="price_sale",
        on_delete=models.DO_NOTHING
    )
    amount = models.IntegerField(
        verbose_name='Quantidade',
        default=1
    )
    product_sale = models.ForeignKey("Sale", related_name='products', default=None, on_delete=models.DO_NOTHING)

    enable_deduction = models.BooleanField('Habilitar desconto', default=False)

    @property
    def price_value(self):
        return self.price.value or 0.00

    def __str__(self):
        return self.product.description