from django.db import models


class Pay(models.Model):
    PAY_MODE = (
        ('D', 'DÉBITO'),
        ('CA', 'CRÉDITO À VISTA'),
        ('CP', 'CRÉDITO PARCELADO'),
        ('A', 'À VISTA'),
        ('CHA', 'CHEQUE À VISTA'),
        ('CHP', 'CHEQUE PARCELADO'),
        ('VP', 'VALE PARCELADO'),
        ('V', 'VALE'),

    )
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=7, verbose_name="Valor")
    mode = models.CharField(choices=PAY_MODE, verbose_name="Modo", max_length=3)
    plots_amount = models.IntegerField(
        verbose_name='Número de parcelas',
        null=True,
        blank=True
    )
    pay_sale = models.ForeignKey("Sale", related_name='payments', default=None, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.value)

    class Meta:
        ordering = ["value"]
