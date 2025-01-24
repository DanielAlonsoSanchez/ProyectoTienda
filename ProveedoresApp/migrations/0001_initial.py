# Generated by Django 5.1.1 on 2024-11-18 21:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DireccionProveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(max_length=255)),
                ('numero', models.CharField(blank=True, max_length=10, null=True)),
                ('ciudad', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=100)),
                ('codigo_postal', models.CharField(max_length=20)),
                ('pais', models.CharField(max_length=100)),
                ('tipo_direccion', models.CharField(choices=[('física', 'Física'), ('envío', 'Envío')], max_length=20, verbose_name='Tipo de Dirección')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Direccion del Proveedor',
                'verbose_name_plural': 'Direccion de los Proveedores',
            },
        ),
        migrations.CreateModel(
            name='ProductosServiciosProveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50, null=True, verbose_name='Productos/Servicios ofrecidos')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Productos o Servicios de Proveedor',
                'verbose_name_plural': 'Productos o Servicios de Proveedores',
            },
        ),
        migrations.CreateModel(
            name='TipoProveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Tipo de Proveedor. Ej: materias primas, servicios...')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Tipo de Proveedor',
                'verbose_name_plural': 'Tipo de Proveedores',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cif', models.CharField(help_text='Introduce un CIF/NIF válido.', max_length=20, unique=True, verbose_name='CIF/NIF')),
                ('correo_electronico', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo electrónico')),
                ('cuenta_bancaria', models.CharField(blank=True, max_length=34, null=True, verbose_name='Cuenta bancaria (IBAN)')),
                ('sitio_web', models.URLField(blank=True, null=True, verbose_name='Sitio web')),
                ('notas', models.TextField(blank=True, null=True, verbose_name='Notas adicionales')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('direcciones', models.ManyToManyField(to='ProveedoresApp.direccionproveedor', verbose_name='Direcciones')),
                ('productos_servicios', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProveedoresApp.productosserviciosproveedor')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProveedoresApp.tipoproveedor')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
    ]
