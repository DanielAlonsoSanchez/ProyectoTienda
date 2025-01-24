# Generated by Django 5.1.1 on 2024-11-18 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProveedoresApp', '0001_initial'),
        ('TiendaApp', '0021_alter_producto_proveedor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ProveedoresApp.proveedor'),
        ),
    ]
