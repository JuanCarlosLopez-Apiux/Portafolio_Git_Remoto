# Generated by Django 2.2.3 on 2020-10-23 21:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0011_auto_20201023_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='fecha_inicio',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='cart',
            name='fecha_termino',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
    ]
