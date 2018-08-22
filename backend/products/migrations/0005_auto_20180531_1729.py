# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-05-31 17:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_employee'),
        ('core', '0003_auto_20180110_2311'),
        ('products', '0004_auto_20170923_1950'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('value', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Valor')),
                ('mode', models.CharField(choices=[('D', 'DÉBITO'), ('CA', 'CRÉDITO À VISTA'), ('CP', 'CRÉDITO PARCELADO'), ('A', 'À VISTA'), ('CHA', 'CHEQUE À VISTA'), ('CHP', 'CHEQUE PARCELADO'), ('VP', 'VALE PARCELADO'), ('V', 'VALE')], max_length=3, verbose_name='Modo')),
                ('plots_amount', models.IntegerField(blank=True, null=True, verbose_name='Número de parcelas')),
            ],
            options={
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('date', models.DateTimeField(verbose_name='Data')),
                ('plot', models.IntegerField(verbose_name='Parcela')),
                ('ploted_value', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Valor da parcela')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='price_sale', to='products.Price', verbose_name='Produto')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_sale', to='products.Product', verbose_name='Produto')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('status', models.CharField(choices=[('C', 'CANCELADA'), ('F', 'FINALIZADA')], max_length=3, verbose_name='Status')),
                ('deduction', models.DecimalField(blank=True, decimal_places=3, max_digits=7, null=True, verbose_name='Desconto')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='client', to='core.Client', verbose_name='Cliente')),
                ('payments', models.ManyToManyField(related_name='payments', to='products.Pay')),
                ('products', models.ManyToManyField(related_name='products', to='products.ProductSale')),
                ('saleswoman', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='employee', to='users.Employee', verbose_name='Vendedora')),
            ],
            options={
                'ordering': ['created', 'status'],
            },
        ),
        migrations.AddField(
            model_name='pay',
            name='plots',
            field=models.ManyToManyField(blank=True, null=True, related_name='plots', to='products.Plot'),
        ),
    ]