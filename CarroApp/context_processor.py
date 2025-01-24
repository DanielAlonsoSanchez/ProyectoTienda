def importe_total_carro(request):
    """
    Calcula el importe total de los productos en el carrito de compras.
    Si no se está autenticado, devuelve un mensaje indicandoque es necesario iniciar sesión.
    """
    total = 0

    # Se comprueba si el usuario está autenticado
    if request.user.is_authenticated:

        # Verifica si existe una clave llamada 'carro' en la sesión del usuario.
        for key, value in request.session["carro"].items():
            total = total + (float(value["precio"]))

    else:
        total="Debes iniciar sesión"

    return {"importe_total_carro": total}
