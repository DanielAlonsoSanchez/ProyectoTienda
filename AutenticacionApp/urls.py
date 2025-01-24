from django.urls import path
from .views import VRegistro, cerrar_sesion, entrar_sesion

urlpatterns = [

    path('', VRegistro.as_view(), name = 'autenticacion'),
    path('cerrar_sesion', cerrar_sesion, name = 'cerrar_sesion'),
    path('entrar_sesion', entrar_sesion, name = 'entrar_sesion'),
]
