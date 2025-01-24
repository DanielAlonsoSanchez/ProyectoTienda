from TiendaApp.models import Producto

class Carro:
    """
    Clase carrito de compras para gestionar los productos añadidos en la sesión actual.
    Permite agregar, eliminar, actualizar y realizar compras de productos.
    """
    def __init__(self,request):
        """
        Inicializa el carrito de compras. Si no existe en la sesión, lo crea como un diccionario vacío.
        """
        self.request = request
        self.session = request.session

        # Intentar obtener el carrito de la sesión. Si no existe, inicializarlo como un diccionario vacío.
        carro = self.session.get("carro")

        if not carro:
            self.carro = self.session["carro"] = {} # Guardar el carrito tanto en self.carro como en la sesión
        else:
            self.carro = carro

    def agregar(self, producto):
        """
        Agrega un producto al carrito. Si el producto ya existe en el carrito, suma su cantidad
        y actualiza el precio total.
        """
        # Comprobar si el producto ya está en el carrito
        if(str(producto.id)) not in self.carro.keys():
            self.carro[producto.id] = {"producto_id": producto.id,
                                        "nombre": producto.nombre,
                                        "precio": producto.precio_con_iva,
                                        "cantidad": 1,
                                        "imagen": producto.imagen.url}

        else:
            # Si el producto ya está, se incrementa su cantidad y su precio total
            for key, value in self.carro.items():
                if key == str(producto.id):
                    value["cantidad"] = value["cantidad"]+1
                    value["precio"] = float(value["precio"]) + producto.precio_con_iva
                    break
        self.guardar_carro()

    def guardar_carro(self):
        """
        Guarda el estado actual del carrito y marca la sesión como modificada
        para asegurarse de que los cambios se reflejen.
        """
        self.session["carro"] = self.carro
        self.session.modified = True

    def eliminar(self, producto):
        """

        """
        producto.id = str(producto.id)
        if producto.id in self.carro:
            del self.carro[producto.id]
            self.guardar_carro()

    def restar_producto(self, producto):
        """
        Reduce la cantidad de un producto en el carrito.
        Si la cantidad llega a 0, el producto se elimina del carrito.
        """
        for key, value in self.carro.items():

            if key == str(producto.id):

                value["cantidad"] = value["cantidad"]-1
                value["precio"] = float(value["precio"]) - producto.precio_con_iva

                # Si la cantidad es menor a 1, eliminar el producto del carrito
                if value["cantidad"] < 1:
                    self.eliminar(producto)
                break
        self.guardar_carro()

    def limpiar_carro(self):
        """
        Vacía completamente el carrito de compras y lo guarda en la sesión.
        """
        self.carro = self.session["carro"] = {} # Lo mismo, Cuidado con este linea, pq 'self.carro' funciona pero 'carro' no?
        self.session.modified = True

    def comprar(self):
        """
        Realiza la compra de todos los productos en el carro.

        Para cada producto en el carrito, verifica si hay suficiente stock disponible.
        Si lo hay, reduce el stock utilizando la función `comprar` del modelo Producto.

        Una vez completada la compra, el carrito se limpia automáticamente.
        """
        for item in self.carro.values():
            producto_id = item['producto_id']
            cantidad = item['cantidad']

            try:
                # Intentar obtener el producto de la base de datos
                producto = Producto.objects.get(id=producto_id)
                print(f"Producto: {producto.nombre}, Cantidad: {cantidad}")

                # Verificar si hay suficiente stock disponible
                if producto.stock_total >= cantidad:

                    resultado = producto.comprar(cantidad)
                    print(resultado)

                else:
                    print(f"No hay suficiente stock para el producto: {producto.nombre}. "
                          f"Stock disponible: {producto.stock_total}, "
                          f"Solicitado: {cantidad}. {producto.disponibilidad}")

            except Producto.DoesNotExist:
                print(f"No se encontró el producto con ID: {producto_id}")

            except ValueError as e:
                print(e)

            except Exception as e:
                print(f"Error inesperado con el producto ID {producto_id}: {e}")

        self.limpiar_carro()  # El carrito se limpia después de realizar la compra
