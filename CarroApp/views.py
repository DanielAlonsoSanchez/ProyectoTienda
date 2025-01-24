from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .carro import Carro
from TiendaApp.models import Producto


def agregar_producto(request, producto_id):

    """Esta función agrega los productos al carrito."""

    carro = Carro(request)
    producto = Producto.objects.get(id=producto_id)
    carro.agregar(producto = producto)

    return redirect("tienda")

def eliminar_producto(request, producto_id):

    """Esta función elimina un producto del carrito."""

    carro = Carro(request)
    producto = Producto.objects.get(id=producto_id)
    carro.eliminar(producto = producto)

    return redirect("tienda")

def restar_producto(request, producto_id):

    """Esta función resta productos del carrito."""

    carro = Carro(request)
    producto = Producto.objects.get(id=producto_id)
    carro.restar_producto(producto = producto)

    return redirect("tienda")

def limpiar_carro(request):

    """Esta función elimina productos del carrito."""

    carro = Carro(request)
    carro.limpiar_carro()

    return redirect("tienda")


def enviar_correo_confirmacion(User, carro):
    """
    Envía un correo de confirmación al usuario con los detalles de la compra.
    """

    print("Itentando enviar correo de confirmacion")

    productos_comprados = []
    total_compra = 0

    # Iterar sobre los productos en el carrito para hacer el resumen de la compra
    for producto in carro.carro.values():
        nombre_producto = producto['nombre']
        cantidad = producto['cantidad']
        precio_con_iva = producto['precio']
        total_producto = precio_con_iva * cantidad

        if cantidad > 0 and precio_con_iva > 0:
            total_producto = precio_con_iva * cantidad

            # Agregar el producto a la lista de productos comprados
            productos_comprados.append(f"{nombre_producto} x {cantidad} = {total_producto:.2f}€")
            total_compra += total_producto

    productos_comprados_str = "\n".join(productos_comprados)

    # Asunto y cuerpo del mensaje
    subject = "Confirmación de Compra"
    message = (
        f"Hola {User.username},\n\n"
        f"Gracias por tu compra. Aquí están los detalles de tu pedido:\n\n"
        f"{productos_comprados_str}\n\n"
        f"Total a pagar (con IVA): {total_compra:.2f}€\n\n"
        f"¡Esperamos que disfrutes de tus productos!\n\n"
        f"Atentamente,\nEl equipo de TecnoMarket"
    )

    # Lista de destinatarios (en este caso, 'tecnomarkettc@gmail.com')
    recipient_list = ['tecnomarkettc@gmail.com']

    # Enviar correo
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,  # Remitente configurado en settings.py
            recipient_list= recipient_list,  # Usar el correo del usuario
            fail_silently=False,
        )
        print("Correo de compra enviado")

    except Exception as e:
        print(f"Error al enviar correo de confirmación: {e}")


def comprar(request):

    """
    Vista para manejar la compra de productos en el carrito.
    """
    carro = Carro(request)

    # Comprobar si el carrito está vacío
    if not carro.carro:
        messages.error(request, "Tu carrito está vacío.")
        return redirect("tienda")

    if request.method == "POST":
        try:
            # Enviar correo de confirmación con los detalles antes de vaciar el carrito
            enviar_correo_confirmacion(request.user, carro)

            # Llamar al método que realiza la compra
            carro.comprar()

            # Vaciar el carrito después de enviar el correo
            carro.limpiar_carro()

            messages.success(request, "Compra realizada con éxito.")

        except Exception as e:
            messages.error(request, f"Error al realizar la compra: {str(e)}")

        return redirect("tienda")

    return redirect("tienda")
