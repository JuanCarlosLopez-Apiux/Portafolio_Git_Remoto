# Generated by Django 3.1.2 on 2020-11-18 23:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_rut_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Fecha_nacimiento',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
