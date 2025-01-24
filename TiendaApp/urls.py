from django.urls import path
from . import views

urlpatterns = [

    path('', views.tienda, name = 'tienda'),
    path('categoria/<int:categoria_id>/', views.categoria, name = "categoria"), # Dentro del <> no se permiten espacios.
    path('reponer_tienda/<int:producto_id>/', views.reponer_tienda, name='reponer_tienda'),
    path('reponer_almacen/<int:producto_id>/', views.reponer_almacen, name='reponer_almacen'),
    path('cambiar_descuento/<int:producto_id>/', views.cambiar_descuento, name='cambiar_descuento'),
]

