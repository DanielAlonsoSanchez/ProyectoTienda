from django.contrib import admin
from .models import DireccionProveedor, ProductosServiciosProveedor, TipoProveedor, Proveedor

# Register your models here.

class DireccionProveedorAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class ProductosServiciosProveedorAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class TipoProveedorAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class ProveedorAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(DireccionProveedor, DireccionProveedorAdmin)
admin.site.register(ProductosServiciosProveedor, ProductosServiciosProveedorAdmin)
admin.site.register(TipoProveedor, TipoProveedorAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
