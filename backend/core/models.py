from django.db import models


class Client(models.Model):
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    name = models.CharField(verbose_name="Nome", max_length=255)
    cpf = models.CharField(verbose_name="CPF", max_length=16)
    rg = models.CharField(verbose_name="RG", max_length=16)
    address = models.TextField(null=True, blank=True, verbose_name="Endereço")
    cep = models.CharField(verbose_name="CEP", max_length=16, null=True, blank=True)
    cellphone = models.TextField(null=True, blank=True, verbose_name="Celular")
    phone = models.TextField(null=True, blank=True, verbose_name="Telefone")
    employee = models.ForeignKey(
        'users.Employee',
        null=True,
        blank=True,
        verbose_name='Vendedora',
        on_delete=models.SET_NULL
    )
    email = models.EmailField(verbose_name="Email", null=True, blank=True)
    facebook = models.CharField(verbose_name="Facebook", max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'cpf']
