# Generated by Django 3.1.2 on 2020-11-19 00:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_fecha_nacimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Fecha_nacimiento',
            field=models.DateField(default=datetime.date.today),
        ),
    ]