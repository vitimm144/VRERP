from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Stock


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

    class Meta:
        ordering = ["id"]



@receiver(post_save, sender=ProductSale)
def save_sale(sender, instance, **kwargs):
    # Decrementando a quantidade de produtos no estoque ao final de cada venda.
    created = kwargs.get('created')
    if created:

        try:
            stock = Stock.objects.filter(product=instance.product, user=instance.product_sale.user)[0]
            if stock:
                stock.amount -= instance.amount
                stock.save()
        except Exception as e:
            print(e)