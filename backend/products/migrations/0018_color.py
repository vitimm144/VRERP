# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-05-12 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20190407_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('code', models.CharField(max_length=9, verbose_name='Código')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Cor',
                'verbose_name_plural': 'Cores',
                'ordering': ['code'],
            },
        ),
    ]
