# Generated by Django 5.1.1 on 2024-11-13 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TiendaApp', '0016_remove_producto_oferta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio_original',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
