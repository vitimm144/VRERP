from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.db import models


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """

    Decorator to create auth_token when Create user signal have been fired

    """
    if created:
        Token.objects.create(user=instance)


class Career(models.Model):

    title = models.CharField(verbose_name='Título', max_length=80, unique=True)
    description = models.TextField(verbose_name='Descrição')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Employee(models.Model):
    picture = models.ImageField(null=True, verbose_name="Foto", upload_to='employees/')
    name = models.CharField(verbose_name="Nome", max_length=255)
    cpf = models.CharField(verbose_name="CPF", max_length=16)
    rg = models.CharField(verbose_name="RG", max_length=16)
    address = models.TextField(null=True, blank=True, verbose_name="Endereço")
    code = models.CharField(unique=True, verbose_name="Código", max_length=255)
    salary = models.DecimalField(decimal_places=2, max_digits=7, verbose_name="Salário")
    career = models.ForeignKey('Career', verbose_name='Função')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'code']


class BehaviorSheet(models.Model):
    BEHAVIOR_TYPES = (
        ('A', 'Advertência'),
        ('P', 'Prêmio'),
    )

    employee = models.ForeignKey('Employee', verbose_name='Funcionário')
    date = models.DateField(verbose_name='Data')
    reason = models.TextField(verbose_name='Motivo')
    behavior_type = models.CharField(verbose_name='Tipo', choices=BEHAVIOR_TYPES, max_length=2)

    def __str__(self):
        return self.behavior_type

    class Meta:
        ordering = ['date', 'behavior_type']
