# Generated by Django 5.1.1 on 2024-11-18 21:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProveedoresApp', '0001_initial'),
        ('TiendaApp', '0018_alter_producto_precio_original'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='categorias',
            new_name='categoria',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='fabricante',
        ),
        migrations.AddField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ProveedoresApp.proveedor'),
        ),
    ]
