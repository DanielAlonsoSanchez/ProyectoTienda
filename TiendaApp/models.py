from django.db import models
from django.core.mail import send_mail
from django.conf import settings

from ProveedoresApp.models import Proveedor, ProductosServiciosProveedor


class CategoriaProducto(models.Model):
    """
    Representa las categorias de los productos.
    """

    nombre = models.CharField(max_length = 50)

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'categoriaProducto'
        verbose_name_plural = 'categoriasProducto'

    def __str__(self):
        return self.nombre

class SeccionProducto(models.Model):
    """
    Representa las secciones de los productos.
    """
    nombre = models.CharField(max_length = 50)

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'seccionProducto'
        verbose_name_plural = 'seccionesProducto'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    """
    Modelo que representa los productos.
    """
    # Información del producto
    nombre = models.CharField(max_length=50, default=None)
    nombre_dado_por_proveedor = models.ForeignKey(ProductosServiciosProveedor, on_delete=models.CASCADE, related_name='productos_nombre', default=None)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='tienda', null=True, blank=True)
    precio_base = models.FloatField(default=0.0)
    precio_de_proveedor = models.ForeignKey(ProductosServiciosProveedor, on_delete=models.CASCADE, related_name='productos_precio', default=None)
    descuento = models.IntegerField(default=0.0)
    sinopsis = models.CharField(max_length=215, null=True, blank=True)
    seccion = models.ForeignKey(SeccionProducto, on_delete=models.CASCADE, default=1)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, default=1)
    iva = models.FloatField(default=21.0)
    beneficios = models.FloatField(default=0.0)

    # Stock y disponibilidad del producto
    stock_en_almacen = models.IntegerField(default=0)       # Cantidad del stock que tenemos en el almacen.
    stock_en_tienda = models.IntegerField(default=0)        # Cantidad del stock que tenemos en la tienda.
    stock_vendido = models.IntegerField(default=0)          # Cantidad del stock que hemos vendido.
    stock_comprado = models.IntegerField(default=0)         # Cantidad del stock que hemos comprado.
    costo_total = models.FloatField(default=0.0)            # Acumula el costo total pagado por el stock comprado.
    pedido_reposicion = models.IntegerField(default=0)      # Pedido siguiente, cada pedido es variable.
    stock_maximo_en_tienda = models.IntegerField(default=0) # Cantidad del stock maximo que podemos tener en tienda.
    stock_maximo_posible = models.IntegerField(default=0)   # Cantidad del stock maximo que podemos tener.
    reponer = models.BooleanField(default=False)            # Campo de reposición
    correo_enviado = models.BooleanField(default=False)     # Control para evitar el envío de correos duplicados

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.nombre


    @property   # Decorador que permite que un metodo funcione como un atributo de la clase.
    def stock_total(self):
        """
        Calcula el stock total actual sumando el stock en tienda y en almacén.
        """
        return self.stock_en_almacen + self.stock_en_tienda


    @property
    def precio_con_descuento(self):
        """
        Calcula el precio con descuento si es que hay uno, de lo contrario, devuelve el precio original.
        """
        if self.descuento > 0:
            return self.precio_base * (1 - (self.descuento / 100))

        else:
            return self.precio_base


    @property
    def precio_con_iva(self):
        """
        Calcula el precio con descuento más IVA.
        """
        precio_descuento = self.precio_con_descuento
        precio_con_iva = precio_descuento * (1 + self.iva / 100)
        return precio_con_iva


    @property
    def precio_base_con_iva(self):
        """
        Calcula el precio base más IVA.
        """
        precio_base_con_iva = self.precio_base * (1 + self.iva / 100)
        return precio_base_con_iva


    @property
    def aviso_falta_stock(self):
        """
        Marca el producto para reposición si el stock total es inferior al 10% del pedido de reposición,
        y envía el correo solo si no se ha notificado previamente.
        """

        if self.stock_total <= self.stock_maximo_posible * 0.1:
            self.reponer = True
            self.save(update_fields=['reponer'])

            # Solo envía el correo si no se ha notificado previamente
            if not self.correo_enviado:
                self.enviar_correo_reposicion()  # Envía el correo si se activa la reposición
                self.correo_enviado = True  # Marca como notificado
                self.save(update_fields=['correo_enviado'])

        else:
            self.reponer = False
            self.save(update_fields=['reponer'])

            # Si el stock se restablece que el correo se envíe de nuevo si es necesario
            self.correo_enviado = False
            self.save(update_fields=['correo_enviado'])

        # Mensaje que saldra en la pagina
        return f"ALERTA: el stock de {self.nombre} está bajo. Se requiere una reposición." if self.reponer else f"No se requiere reposición."


    def enviar_correo_reposicion(self):
        """
        Envía un correo al administrador cuando el stock está bajo.
        """

        print("Enviando correo de reposición")

        # Asunto del correo
        subject = f"Falta de stock: {self.nombre}"

        # Cuerpo del mensaje
        message = (
            f"ALERTA: El stock del producto '{self.nombre}' está bajo.\n"
            f"Stock total actual: {self.stock_total}\n"
            f"Se requiere una reposición urgentemente.\n\n"
            f"Por favor, gestiona la reposición lo antes posible."
        )

        # Lista de destinatarios (en este caso, 'tecnomarkettc@gmail.com')
        recipient_list = ['tecnomarkettc@gmail.com']

        # Enviar el correo
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,  # Utiliza el correo configurado en settings.py
            recipient_list=recipient_list,
            fail_silently=False,
        )

        print(f"Correo de reposición enviado")

    def comprar(self, cantidad):
        """
        Realiza la compra de una cantidad de productos,
        descontando primero del stock en tienda y luego del almacén,
        y actualiza los beneficios obtenidos por la venta.
        """
        if self.stock_total == 0:
            raise ValueError(f"No hay suficiente stock de {self.nombre} para la cantidad solicitada ({cantidad}).")

        if cantidad > self.stock_total:
            raise ValueError(f"No hay suficiente stock de {self.nombre} para la cantidad solicitada ({cantidad}).")

        # Descuenta del stock en tienda y luego en almacén
        if self.stock_en_tienda >= cantidad:
            self.stock_en_tienda -= cantidad
        else:
            restante = cantidad - self.stock_en_tienda
            self.stock_en_tienda = 0

            # Verifica que no se vuelva negativo el stock en almacén
            if self.stock_en_almacen >= restante:
                self.stock_en_almacen -= restante
            else:
                raise ValueError(f"No hay suficiente stock en el almacén para completar la compra de {self.nombre}.")

        # Actualiza el total vendido
        self.stock_vendido += cantidad

        # Calcula el valor de la compra y actualizar beneficios
        valor_compra = self.precio_con_iva * cantidad
        self.beneficios += valor_compra

        # Guarda cambios en stock en tienda, almacén y total vendido
        self.save(update_fields=['stock_en_tienda', 'stock_en_almacen', 'stock_vendido','beneficios',])

        # Verifica si se necesita reabastecimiento o si se agotó el stock
        self.aviso_falta_stock()

        return "Compra realizada"


    def reponer_tienda_desde_almacen(self, cantidad_fija):
        """
        Repone el stock en tienda a partir del stock en almacén.
        Si no hay suficiente stock en almacén, solo se repone lo disponible.
        """
        if self.stock_en_almacen <= 0:
            return f"No hay suficiente stock en almacén para reponer {cantidad_fija} unidades a la tienda."

        if self.stock_en_tienda >= self.stock_maximo_en_tienda:
            return f"No hay espacio suficiente en tienda para reponer más unidades"

        # Calcula la cantidad que realmente se puede reponer sin que almacén quede en negativo
        cantidad_restante_en_almacen = min(cantidad_fija, self.stock_en_almacen)

        # Calcula la cantidad que realmente se puede añadir sin sobrepasar el stock máximo posible de la tienda
        stock_faltante_tienda = min(cantidad_fija, self.stock_maximo_en_tienda - self.stock_en_tienda)

        # Determina la cantidad que realmente se puede reponer
        cantidad_reponer = min(cantidad_restante_en_almacen, stock_faltante_tienda)

        # Actualiza los valores de stock
        self.stock_en_almacen -= cantidad_reponer
        self.stock_en_tienda += cantidad_reponer

        self.save(update_fields=['stock_en_almacen', 'stock_en_tienda'])

        return f"Se han repuesto {cantidad_reponer} unidades del almacén a la tienda del producto: {self.nombre}. Stock en tienda: {self.stock_en_tienda}, " \
               f"Stock en almacén: {self.stock_en_almacen}"


    def reponer_almacen(self, cantidad_reposicion):
        """
        Repone el stock en almacén hasta un número dado por 'cantidad_reposicion', sin superar el 'stock_maximo_posible'.
        El costo de reposición se añade al costo total.
        """
        if self.stock_en_almacen >= self.stock_maximo_posible:
            return "El almacén ya está en su capacidad máxima. No es necesario reponer más."

        # Calcula la cantidad que se puede añadir sin sobrepasar el stock máximo
        cantidad_reponer = min(cantidad_reposicion, self.stock_maximo_posible - self.stock_en_almacen)

        # Calcula el costo total de la reposición
        costo_reposicion = self.precio_de_proveedor.precio * cantidad_reponer

        # Actualiza el stock en almacén
        self.stock_en_almacen += cantidad_reponer

        # Actualiza el stock comprado
        self.stock_comprado += cantidad_reponer

        # Suma el costo de reposición al costo total
        self.costo_total += costo_reposicion

        self.save(update_fields=['stock_en_almacen', 'stock_comprado', 'costo_total'])

        return f"Se han repuesto {cantidad_reponer} unidades al almacén del producto: {self.nombre}. " \
               f"Stock en almacén: {self.stock_en_almacen} / Costo de reposición: {costo_reposicion:.2f}€ / Costo total acumulado: {self.costo_total:.2f}€"


    def cambiar_descuento(self, porcentaje_descuento):
        """
        Modifíca el descuento del producto.
        """
        if porcentaje_descuento < 0:
            porcentaje_descuento = 0

        elif porcentaje_descuento > 100:
            porcentaje_descuento = 100

        # Establece el nuevo descuento
        self.descuento = porcentaje_descuento

        self.save(update_fields=['descuento'])

        return f"El descuento actual del producto: {self.nombre} es de un: {self.descuento}% "


    def calcular_beneficios_netos(self):
        """
        Calcula los beneficios netos como la diferencia entre los ingresos por ventas y el costo total.
        """
        # Ingresos por ventas
        ingresos = self.stock_vendido * self.precio_con_iva

        # Beneficio neto
        beneficios_netos = ingresos - self.costo_total

        return beneficios_netos
