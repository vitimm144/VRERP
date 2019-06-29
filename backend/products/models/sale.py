from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

import locale


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
        on_delete=models.SET_NULL
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        verbose_name="Loja",
        null=True,
        on_delete=models.SET_NULL
    )
    whole_sale = models.BooleanField(verbose_name="Atacado?", default=False)

    @property
    def total(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        result = self.payments.all().aggregate(models.Sum('value'))
        valor = locale.currency(
            result.get('value__sum', 0.00) or 0.00
        )
        return valor

    @property
    def saleswoman_str(self):
        return self.saleswoman.name

    @property
    def user_str(self):
        return self.user.username

    def __str__(self):
        return self.status

    class Meta:
        ordering = ['created', 'status']
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
