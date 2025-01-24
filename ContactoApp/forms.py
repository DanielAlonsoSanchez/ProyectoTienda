from django import forms

class FormularioContacto(forms.Form):
    """
    Crea los datos que necesita el formulario
    """
    nombre = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu nombre'}),
        label="Nombre"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu correo'}),
        label="Email"
    )
    contenido = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu mensaje'}),
        label="Contenido"
    )
