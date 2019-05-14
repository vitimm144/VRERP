from django.db import models


class Plot(models.Model):
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    date = models.DateTimeField('Data')
    plot = models.IntegerField(verbose_name='Parcela')
    ploted_value = models.DecimalField(
        decimal_places=2,
        max_digits=7,
        verbose_name="Valor da parcela"
    )
    plot_pay = models.ForeignKey(
        'Pay',
        related_name='plots',
        null=True,
        blank=True,
        on_delete = models.DO_NOTHING
    )
    class Meta:
        ordering = ["id"]
