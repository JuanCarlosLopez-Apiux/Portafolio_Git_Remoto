# Generated by Django 3.1.2 on 2020-11-30 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_product_e_id_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='e_id_empresa',
            field=models.ForeignKey(db_column='e_id_empresa', on_delete=django.db.models.deletion.DO_NOTHING, to='products.empresa'),
        ),
    ]