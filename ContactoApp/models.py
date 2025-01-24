from django.db import models

class Contacto(models.Model):
    """
    Almacena los datos de contacto enviados por los usuarios.
    """
    nombre = models.CharField(max_length=50)
    email = models.EmailField(default="")
    contenido = models.TextField(default="")

    def __str__(self):
        return self.nombre
