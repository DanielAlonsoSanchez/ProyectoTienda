from django.shortcuts import render
from ServiciosApp.models import Servicio


def servicios(request):
    """
    Vista que maneja la página de los servicios ofrecidos.
    """
    servicios = Servicio.objects.all()
    return render(request, "ServiciosApp/servicios.html", {'servicios': servicios})
