# Generated by Django 2.2.3 on 2020-10-22 06:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_auto_20201022_0333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='cantidad_de_dias',
        ),
        migrations.AlterField(
            model_name='cart',
            name='fecha_inicio',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 10, 22, 3, 35, 25, 616797)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='fecha_termino',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 10, 22, 3, 35, 25, 616797)),
        ),
    ]
