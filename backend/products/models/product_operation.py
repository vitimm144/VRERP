from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Stock
from products.models import StockOperation
from django.db import transaction


class ProductOperation(models.Model):

    OPERATION_REASONS = (
        ('TF', 'Transferência'),
        ('TR', 'Troca'),
        ('V', 'Venda'),
        ('C', 'Correção'),
    )

    OPERATION_TYPES = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )


    date  = models.DateTimeField(verbose_name='Data', auto_now_add=True)
    reason = models.CharField(verbose_name='Motivo', choices=OPERATION_REASONS, max_length=2 )
    type = models.CharField(verbose_name='Tipo', choices=OPERATION_TYPES, max_length=2 )
    store = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Loja",
        related_name="store",
        on_delete=models.DO_NOTHING
    )

    product = models.ForeignKey("Product", verbose_name="Produto", on_delete=models.DO_NOTHING)
    amount = models.IntegerField(
        verbose_name='Quantidade'
    )

    def __str__(self):
        return self.reason

    @property
    def code(self):
        return self.product.code

    class Meta:
        ordering = ["id", "date"]



@receiver(post_save, sender=ProductOperation)
def save_product_operation(sender, instance, **kwargs):
    # Metodo para manipular o objeto de estoque
    created = kwargs.get('created')
    if created:

        try:
            with transaction.atomic():
                #Buscando o estoque para realizar a operação.
                if instance.type == 'E':
                    stock = Stock.objects.filter(product=instance.product, user=instance.store)[0]
                    if not stock:
                        stock = Stock.objects.create(
                            product=instance.product,
                            user=instance.dst,
                            amount=instance.amount
                        )
                    else:
                        stock.amount += instance.amount


                else:
                    stock = Stock.objects.filter(product=instance.product, user=instance.store)[0]
                    stock.amount -= instance.amount

                stock.save()

                StockOperation.objects.create(
                    stock=stock,
                    product_operation = instance,
                )
        except Exception as e:
            print(e)