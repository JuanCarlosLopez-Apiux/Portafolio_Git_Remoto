# Generated by Django 3.1.2 on 2020-11-30 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20201118_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
