from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import os
from django.conf import settings
from django.db.models import F, FloatField, ExpressionWrapper, Q
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from TiendaApp.models import Producto, CategoriaProducto, SeccionProducto

matplotlib.use('Agg')  # Usar el backend sin GUI para poder generar gráficos en el servidor sin necesidad de una interfaz gráfica

def tienda(request):
    """
    Vista principal de la tienda. Muestra todos los productos disponibles
    y permite filtrarlos y ordenarlos por diferentes criterios.

    También genera gráficas sobre las ventas y beneficios de los productos.
    """
    # Obtener todos los productos y categorias
    productos = Producto.objects.all()
    categorias = CategoriaProducto.objects.all()

    # Filtrar por término de búsqueda (cuando haga falta)
    query = request.GET.get('q', '')  # Obtener el término de búsqueda de la URL

    if query:
        productos = productos.filter(Q (nombre__icontains=query))

    # Calculamos el precio con IVA
    # ExpressionWrapper esta mas optimizado para consultas grandes.
    productos = productos.annotate(precio_con_iva_calculado = ExpressionWrapper(
                                   F('precio_base') * (1 + F('iva') / 100), output_field = FloatField()))

    # Obtener el criterio de ordenación de los productos
    criterio_orden = request.GET.get('ordenar', '')

    if criterio_orden == 'precio_asc':
        productos = productos.order_by('precio_con_iva_calculado')

    elif criterio_orden == 'precio_desc':
        productos = productos.order_by('-precio_con_iva_calculado')

    elif criterio_orden == 'ventas_desc':
        productos = productos.order_by('-stock_vendido')

    elif criterio_orden == 'nombre_asc':
        productos = productos.order_by('nombre')

    elif criterio_orden == 'nombre_desc':
        productos = productos.order_by('-nombre')

    # Creamos las listas para los datos de la gráfica
    ventas_totales = []
    beneficios = []
    nombres_productos = []

    # Recopilación de los datos necesarios para las gráficas
    for producto in productos:
        nombres_productos.append(producto.nombre)
        ventas_totales.append(producto.stock_vendido)
        beneficios.append(producto.calcular_beneficios_netos())

    # Creación de las gráficas
    grafica_ventas = generar_grafica_ventas(nombres_productos, ventas_totales)
    grafica_beneficios = generar_grafica_beneficios(nombres_productos, beneficios)

    # Renderizar la respuesta con las gráficas y los productos
    return render(request, "TiendaApp/tienda.html", {
        'productos': productos,
        'grafica_ventas': grafica_ventas,
        'grafica_beneficios': grafica_beneficios,
        'categorias': categorias,
    })

def generar_grafica_ventas(nombres_productos, ventas_totales):
    """
    Esta función genera una gráfica de barras que muestra las ventas totales de cada producto.

    La gráfica se guarda como una imagen PNG en el sistema de archivos  y la ruta relativa
    a la imagen se devuelve para poder mostrarla.
    """
    # La ruta donde se guardará la gráfica
    grafica_ventas_path = os.path.join(settings.MEDIA_ROOT, 'grafica_ventas.png')

    # Crear gráfico de ventas
    plt.figure(figsize=(15, 9))
    sns.set_palette("Blues")  # Usar una paleta de colores agradable
    bars = plt.bar(nombres_productos, ventas_totales, color='skyblue')

    # Títulos
    plt.title("Ventas Totales por Producto", fontsize=16, fontweight='bold')
    plt.xlabel("Producto", fontsize=14)
    plt.ylabel("Cantidad Vendida", fontsize=14)

    # Rotación de etiquetas y tamaño de fuente
    plt.xticks(rotation=0, ha='right', fontsize=12)
    plt.yticks(fontsize=12)

    # Se añade una cuadrícula
    plt.grid(axis='y', linestyle='-', alpha=0.7)

    # Etiquetas con el valor de las barras
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, str(int(yval)), ha='center', fontsize=12, color='black')


    # Se guarda la imagen en un archivo
    plt.tight_layout()  # Ajustar márgenes
    plt.savefig(grafica_ventas_path, format='png')
    plt.close()

    # Devolver la URL de la imagen
    return os.path.join(settings.MEDIA_URL, 'grafica_ventas.png')


def generar_grafica_beneficios(nombres_productos, beneficios_netos):
    """
    Esta función genera una gráfica de barras que muestra los beneficios netos de cada producto.

    La gráfica se guarda como una imagen PNG en el sistema de archivos  y la ruta relativa
    a la imagen se devuelve para poder mostrarla.
    """
    # La ruta donde se guardará la gráfica
    grafica_beneficios_path = os.path.join(settings.MEDIA_ROOT, 'grafica_beneficios.png')

    # Crear gráfico de beneficios
    plt.figure(figsize=(15, 9))
    bars = plt.bar(nombres_productos, beneficios_netos, color='lightgreen')

    # Títulos
    plt.title("Beneficios por Producto", fontsize=16, fontweight='bold')
    plt.xlabel("Producto", fontsize=14)
    plt.ylabel("Beneficio (€)", fontsize=14)

    # Rotación de etiquetas y tamaño de fuente
    plt.xticks(rotation=0, ha='right', fontsize=12)
    plt.yticks(fontsize=12)

    # Se añade una cuadrícula
    plt.grid(axis='y', linestyle='-', alpha=0.7)

   # Etiquetas con el valor de las barras
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 5, f"€{yval:.2f}", ha='center', fontsize=12, color='black')

    # Se guarda la imagen en un archivo
    plt.tight_layout()  # Ajustar márgenes
    plt.savefig(grafica_beneficios_path, format='png')
    plt.close()

    # Devolver la URL de la imagen
    return os.path.join(settings.MEDIA_URL, 'grafica_beneficios.png')


def categoria(request, categoria_id):
    """
    Esta función maneja la visualización de los productos de una categoría específica.
    """
    categoria = get_object_or_404(CategoriaProducto, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    categorias = CategoriaProducto.objects.all()
    return render(request, 'TiendaApp/categorias/categoria.html', {'categoria': categoria, 'productos': productos, 'categorias': categorias,})

def reponer_tienda(request, producto_id):
    """
    Esta función permite reponer el stock de un producto en la tienda,
    tomando de referencía el stock disponible en el almacén.
    """
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad_reposicion = int(request.POST.get('cantidad_reposicion', producto.stock_maximo_en_tienda))
    mensaje = producto.reponer_tienda_desde_almacen(cantidad_reposicion)
    messages.success(request, mensaje)
    return redirect('tienda')

def reponer_almacen(request, producto_id):
    """
    Esta función permite reponer el stock de un producto desde el almacén.
    Valida que la cantidad proporcionada sea válida antes de realizar la reposición.
    """
    try:
        producto = get_object_or_404(Producto, id=producto_id)  # Obtener el producto de la base de datos

        cantidad_reposicion = request.POST.get('cantidad_reposicion', '').strip()  # Obtener la cantidad del formulario

        # Se verifica si se ha proporcionado una cantidad válida
        if not cantidad_reposicion.isdigit() or int(cantidad_reposicion) <= 0:
            messages.error(request, "Por favor ingresa una cantidad válida para reposición.")
            return redirect('tienda')

        cantidad_reposicion = int(cantidad_reposicion)

        # Llamada al método de reposición
        mensaje = producto.reponer_almacen(cantidad_reposicion)
        messages.success(request, mensaje)
        return redirect('tienda')

    except Exception as e:
        messages.error(request, f"Ocurrió un error: {str(e)}")
        return redirect('tienda')

def cambiar_descuento(request, producto_id):
    """
    Esta función permite cambiar el porcentaje de descuento de un producto (solo entre 0-100).
    """
    producto = get_object_or_404(Producto, id=producto_id)

    # Obtener el porcentaje de descuento desde el formulario
    try:
        porcentaje_descuento = int(request.POST.get('porcentaje_descuento', 0))
    except ValueError:
        messages.error(request, "El porcentaje de descuento debe ser un número válido.")
        return redirect('tienda')

    # Nos aseguramos de que el descuento esté dentro del rango válido
    if porcentaje_descuento < 0 or porcentaje_descuento > 100:
        messages.error(request, "El descuento debe estar entre 0 y 100.")
        return redirect('tienda')

    # Llamar al método para cambiar el descuento
    mensaje = producto.cambiar_descuento(porcentaje_descuento)
    messages.success(request, mensaje)
    return redirect('tienda')
