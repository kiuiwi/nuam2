from django import forms
from .models import Usuario, Persona, Documento

# ---------------------------
# FORMULARIO DE USUARIO
# ---------------------------
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre_usuario", "contrasena", "usuario_tipo"]
        widgets = {
            "contrasena": forms.PasswordInput()
        }

# ---------------------------
# FORMULARIO DE PERSONA
# ---------------------------
class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            "nombres", "apellidos", "telefono",
            "email", "direccion", "pais", "region"
        ]

# ---------------------------
# FORMULARIO DE DOCUMENTO
# ---------------------------
class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ["usuario", "documento_nombre", "documento_tipo", "archivo"]
