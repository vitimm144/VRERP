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


class WorkSchedule(models.Model):
    MONTHS = (
        ('JAN', 'Janeiro'),
        ('FEV', 'Feveireiro'),
        ('MAR', 'Março'),
        ('ABR', 'ABRIL'),
        ('MAI', 'Maio'),
        ('JUN', 'Junho'),
        ('JUL', 'Julho'),
        ('AGO', 'Agosto'),
        ('SET', 'Setembro'),
        ('OUT', 'Outubro'),
        ('NOV', 'Novembro'),
        ('DEZ', 'Dezembro'),
    )

    month = models.CharField(verbose_name='Mês', choices=MONTHS, max_length=3)
    year = models.CharField(verbose_name='Ano', max_length=4)
    shift_start = models.TimeField(verbose_name='Inicio do turno', default='08:30')
    shift_end = models.TimeField(verbose_name='Fim do turno', default='18:00')
    employee = models.ForeignKey('Employee', verbose_name='Funcionário')

    @property
    def employee_name(self):
        name = self.employee.name
        return name

    def __str__(self):
        return self.month

    class Meta:
        ordering = ['month', 'year']
        verbose_name = "Controle de Ponto"
        verbose_name_plural = "Controles de pontos"


class WorkShift(models.Model):
    ALLOWANCES = (
        ('FO', 'Folga'),
        ('AT', 'Atestado'),
        ('DE', 'Declaração'),
        ('DR', 'Descanso Remunerado'),
    )
    m_start = models.TimeField(verbose_name='Inicio do turno da manhã', default='08:30')
    m_end = models.TimeField(verbose_name='Fim do turno da manhã', default='12:30')
    a_start = models.TimeField(verbose_name='Inicio do turno da tarde', default='13:30')
    a_end = models.TimeField(verbose_name='Fim do turno da tarde', default='18:00')
    e_start = models.TimeField(verbose_name='Inicio da hora extra', null=True, blank=True)
    e_end = models.TimeField(verbose_name='Fim da hora extra', null=True, blank=True)
    date = models.DateField(verbose_name='Data', default='2018-01-01')
    work_schedule = models.ForeignKey('WorkSchedule', verbose_name='Ponto', related_name="work_shifts")
    allowance = models.CharField(verbose_name='Abonos', choices=ALLOWANCES, null=True, blank=True, max_length=2)
    reduced_day = models.BooleanField(verbose_name='Jornada reduzida', default=False)

    def __str__(self):
        return "{0} - {1}".format(self.m_start, self.a_end)

    class Meta:
        ordering = ['m_start', 'a_end']
        verbose_name = "Horário trabalhado"
        verbose_name_plural = "Horários trabalhados"
