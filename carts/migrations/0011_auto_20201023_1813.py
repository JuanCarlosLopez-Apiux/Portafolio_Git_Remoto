# Generated by Django 2.2.3 on 2020-10-23 21:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0010_auto_20201023_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='fecha_inicio',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 10, 23, 21, 13, 12, 510258, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='fecha_termino',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 10, 23, 21, 13, 12, 510258, tzinfo=utc)),
        ),
    ]
