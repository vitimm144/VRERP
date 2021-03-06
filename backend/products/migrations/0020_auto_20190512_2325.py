# Generated by Django 2.2.1 on 2019-05-12 23:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_product_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='plot_pay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='plots', to='products.Pay'),
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=255, verbose_name='Código'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.Product', verbose_name='Produto'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Loja'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('code', 'size', 'color')},
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['code', 'size', 'color'], name='products_pr_code_283367_idx'),
        ),
    ]
