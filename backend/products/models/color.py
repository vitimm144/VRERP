from django.db import models


class Color(models.Model):
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    code = models.CharField(verbose_name='Código', max_length=9)
    name = models.CharField(verbose_name='Nome', max_length=255)

    class Meta:
        ordering = ['code',]
        verbose_name = "Cor"
        verbose_name_plural = "Cores"

    def __str__(self):
        return self.name
