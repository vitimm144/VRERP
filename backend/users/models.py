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


