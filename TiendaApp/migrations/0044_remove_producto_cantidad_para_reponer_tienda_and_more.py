# Generated by Django 5.1.1 on 2024-11-20 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TiendaApp', '0043_rename_precio_original_producto_precio_base'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='cantidad_para_reponer_tienda',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='stock_maximo_en_tienda',
        ),
    ]
