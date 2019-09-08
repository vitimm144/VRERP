from django.db import models


class StockOperation(models.Model):
    created = models.DateTimeField(verbose_name='Data', auto_now_add=True)
    stock = models.ForeignKey(
        'Stock',
        related_name='stock_stock_operation',
        on_delete=models.DO_NOTHING
    )
    product_operation = models.ForeignKey(
        'ProductOperation',
        related_name='product_operation',
        on_delete=models.DO_NOTHING
    )

    class Meta:
        ordering = ["id", "created"]
        verbose_name = "Operação de Estoque"
        verbose_name_plural = "Operações de Estoque"

    def __str__(self):
        return self.product_operation.type
