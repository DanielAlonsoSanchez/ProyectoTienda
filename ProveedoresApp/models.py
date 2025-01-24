from django.db import models
from phonenumber_field.formfields import PhoneNumberField

class TipoProveedor(models.Model):
    """
    Define el tipo de proveedor.
    """
    nombre = models.CharField(verbose_name="Tipo de Proveedor. Ej: materias primas, servicios...", max_length = 50)

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'Tipo de Proveedor'
        verbose_name_plural = 'Tipo de Proveedores'

    def __str__(self):
        return self.nombre

class ProductosServiciosProveedor(models.Model):
    """
    Representa los productos o servicios ofrecidos por los proveedores.
    """
    nombre = models.CharField(verbose_name="Productos/Servicios ofrecidos", blank=True, null=True, max_length = 50)
    precio = models.FloatField(default=0.0)

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'Productos o Servicios de Proveedor'
        verbose_name_plural = 'Productos o Servicios de Proveedores'

    def __str__(self):
        return self.nombre

class DireccionProveedor(models.Model):
    """
    Representa las direcciones asociadas a los proveedores.
    """
    calle = models.CharField(max_length=255)
    numero = models.CharField(max_length=10, blank=True, null=True)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    pais = models.CharField(max_length=100)
    tipo_direccion = models.CharField(
        max_length=20,
        choices=(("física", "Física"), ("envío", "Envío")),
        verbose_name="Tipo de Dirección"
    )

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'Direccion del Proveedor'
        verbose_name_plural = 'Direccion de los Proveedores'

    def __str__(self):
        return f"{self.calle}, {self.ciudad}, {self.pais}"

class Proveedor(models.Model):
    """
    Modelo principal de los proveedores con datos generales y relacionados con productos y servicios.
    """
    # Datos Generales
    nombre = models.CharField(max_length = 100)
    cif = models.CharField(
        max_length=20,
        unique = True,  # Debe ser único
        verbose_name="CIF/NIF",
        help_text="Introduce un CIF/NIF válido.")

    correo_electronico = models.EmailField(verbose_name="Correo electrónico", blank=True, null=True)
    telefono = PhoneNumberField(
        region="ES",
        label="Número de teléfono",
        help_text="Incluye el código de país, ej. +34 para España."
    )

    telefono_adicional = PhoneNumberField(
        region="ES",
        label="Número de teléfono",
        help_text="Incluye el código de país, ej. +34 para España."
    )
    direcciones = models.ManyToManyField(DireccionProveedor, verbose_name="Direcciones")
    cuenta_bancaria = models.CharField(max_length=34, verbose_name="Cuenta bancaria (IBAN)", blank=True, null=True)

    # Información Extra
    tipo = models.ForeignKey(TipoProveedor, on_delete=models.CASCADE)
    productos_servicios = models.ManyToManyField(ProductosServiciosProveedor, verbose_name="Productos")
    sitio_web = models.URLField(verbose_name="Sitio web", blank=True, null=True)
    notas = models.TextField(verbose_name="Notas adicionales", blank=True, null=True)

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.nombre
