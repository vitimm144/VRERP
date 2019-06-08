from django.db import models


class PriceManager(models.Manager):
    def get_queryset(self):
        return super(PriceManager, self).get_queryset().filter(in_use=True)


class Price(models.Model):
    objects = PriceManager()
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    in_use = models.BooleanField(default=True, verbose_name="Em uso")
    value = models.DecimalField(decimal_places=2, max_digits=7, verbose_name="Valor")
    product = models.ForeignKey(
        "Product",
        verbose_name="Produto",
        related_name="products",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.value)

    def delete(self, using=None):
        self.in_use = False
        self.save()

    def set_in_use(self):
        self.in_use = False
        self.save()

    class Meta:
        ordering = ["value"]