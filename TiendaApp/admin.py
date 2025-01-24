from django.contrib import admin
from .models import CategoriaProducto, SeccionProducto, Producto


class CategoriaProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class SeccionProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(CategoriaProducto, CategoriaProductoAdmin)
admin.site.register(SeccionProducto, SeccionProductoAdmin)
admin.site.register(Producto, ProductoAdmin)
