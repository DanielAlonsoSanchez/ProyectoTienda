from django.shortcuts import render, HttpResponse
from CarroApp.carro import Carro


def home(request):
    """
    Vista que maneja la página de inicio de la tienda web.

    También se asegura de que el carrito de compras esté disponible
    para mostrar el contenido del carrito en la interfaz de usuario.
    """
    carro = Carro(request)  # Crea una instancia del carrito de compras pasando el objeto request
    return render(request, "ProyectoTiendaWebApp/home.html")
