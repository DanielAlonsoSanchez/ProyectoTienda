from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nombre de usuario'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirma tu contraseña'})

class VRegistro(View):

    def get(self, request):
        form = CustomUserCreationForm() # Se esta usando CustomUserCreationForm
        return render(request, "AutenticacionApp/registro/registro.html", {"form":form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST) # Se esta usando CustomUserCreationForm

        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("home")

        else:
            for msg in form.error_messages:
                messages.error(request,form.error_messages[msg])
            return render(request, "AutenticacionApp/registro/registro.html", {"form":form})


class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nombre de usuario'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Contraseña'})

def entrar_sesion(request):

    if request.method == "POST":
        form=CustomAuthenticationForm(request,data=request.POST)    #Se esta usando CustomAuthenticationForm CustomUserCreationForm

        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contrasena = form.cleaned_data.get("password")
            usuario = authenticate(username = nombre_usuario, password = contrasena)

            if usuario is not None:
                login(request, usuario)
                return redirect("home")
            else:
                messages.error(request, "Usuario NO valido")

        else:
            messages.error(request, "La contraseña o el usuario no son correctos")

    form = CustomAuthenticationForm()
    return render(request,"AutenticacionApp/login/login.html", {"form":form})


def cerrar_sesion(request):

    logout(request)
    return redirect('home')

