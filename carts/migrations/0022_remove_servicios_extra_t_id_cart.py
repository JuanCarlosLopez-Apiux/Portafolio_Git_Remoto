# Generated by Django 3.1.2 on 2020-11-30 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0021_servicios_extra_t_id_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicios_extra',
            name='t_id_cart',
        ),
    ]