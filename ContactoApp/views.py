from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from smtplib import SMTPException

from .forms import FormularioContacto

def contacto(request):
    """
    Maneja el formulario de contacto y envia un correo electrónico.
    """
    # Inicializa el formulario vacío para mostrarlo en la página
    formulario_contacto = FormularioContacto()

    # Verifica si la solicitud es un POST
    if request.method == "POST":

        # Obtiene los datos del formulario enviados a través de POST
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        contenido = request.POST.get("contenido")

        # Aqui se crea el mensaje de correo electrónico
        email_mensaje = EmailMessage(
            subject="Mensaje de contacto desde la web",
            body=f"El usuario {nombre} con la dirección {email} escribe lo siguiente:\n\n{contenido}",
            from_email=email,                # Dirección de Gmail para el remitente
            to=["tecnomarkettc@gmail.com"],  # Dirección a la que enviar el correo
            reply_to=[]                      # Dirección del usuario para responder
        )

        try:
            email_mensaje.send()
            messages.success(request, "Correo enviado correctamente.")
            return redirect("/contacto")

        except SMTPException as e:
            print(f"Error al enviar el correo: {e}")
            messages.error(request, "No se pudo enviar el correo. Inténtalo nuevamente más tarde.")
            return redirect("/contacto")

        except Exception as e:
            print(f"Error inesperado: {e}")
            messages.error(request, "Ocurrió un error inesperado.")
            return redirect("/contacto")

    return render(request, "ContactoApp/contacto.html", {'formulario': formulario_contacto})
