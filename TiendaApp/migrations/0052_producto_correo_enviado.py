# Generated by Django 5.1.1 on 2024-12-20 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TiendaApp', '0051_remove_producto_correo_enviado'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='correo_enviado',
            field=models.BooleanField(default=False),
        ),
    ]
