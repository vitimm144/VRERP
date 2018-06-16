from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from products.models import Stock


class Sale(models.Model):

    STATUS = (
        ('C', 'CANCELADA'),
        ('F', 'FINALIZADA'),

    )

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    saleswoman = models.ForeignKey(
        "users.Employee",
        related_name='employee',
        on_delete=models.DO_NOTHING,
        verbose_name="Vendedora"
    )
    status = models.CharField(choices=STATUS, verbose_name="Status", max_length=3)
    deduction = models.DecimalField(
        verbose_name="Desconto",
        null=True,
        blank=True,
        max_digits=7,
        decimal_places=3
    )
    client = models.ForeignKey(
        "core.Client",
        verbose_name="Cliente",
        null=True,
        blank=True,
        related_name="client",
        on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        verbose_name="Loja",
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.status

    class Meta:
        ordering = ['created', 'status']


@receiver(post_save, sender=Sale)
def save_sale(sender, instance, **kwargs):
    # Decrementando a quantidade de produtos no estoque ao final de cada venda.
    for psale in instance.products.all():
        psale.product.amount = psale.product.amount - psale.amount
        psale.product.save()
        try:
            stock = Stock.objects.filter(product=psale.product, user=psale.user)[0]
            if stock:
                stock.amount -= psale.amount
                stock.save()
        except Exception as e:
            print(e.message)
            pass

