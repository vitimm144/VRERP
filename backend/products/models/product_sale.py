from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Stock, ProductOperation


class ProductSale(models.Model):
    product = models.ForeignKey(
        "Product",
        verbose_name="Produto",
        related_name="product_sale",
        null=True,
        on_delete=models.SET_NULL
    )
    price = models.ForeignKey(
        "Price",
        verbose_name="Preço",
        related_name="price_sale",
        null=True,
        on_delete=models.SET_NULL
    )
    amount = models.IntegerField(
        verbose_name='Quantidade',
        default=1
    )
    product_sale = models.ForeignKey(
        "Sale",
        related_name='products',
        default=None,
        null=True,
        on_delete=models.SET_NULL
    )

    enable_deduction = models.BooleanField('Habilitar desconto', default=False)

    @property
    def price_value(self):
        return self.price.value or 0.00

    @property
    def price_whole_sale(self):
        return self.price.whole_sale_price or 0.00

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
            productOperation = ProductOperation.objects.create(
                reason='V',
                type='S',
                store=instance.product_sale.user,
                product=instance.product,
                amount=instance.amount
            )
        except Exception as e:
            print(e)