from django import forms
from .models import Usuario
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UsuarioCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    cedula = forms.CharField(label='Cédula')  # Aquí pedimos solo la cédula en texto claro
    telefono = forms.CharField(label='Teléfono', required=False)  # Agregamos teléfono también

    class Meta:
        model = Usuario
        fields = ('correo_claro', 'nombre', 'telefono', 'empresa', 'rol', 'cedula')  # Asegúrate que estos campos estén

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return pass2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.correo = self.cleaned_data["correo_claro"]
        user.cedula = self.cleaned_data["cedula"]  # Esto usará el setter para encriptar la cédula
        user.telefono = self.cleaned_data["telefono"]  # Guardamos el teléfono directamente
        if commit:
            user.save()
        return user

class UsuarioChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    cedula = forms.CharField(label='Cédula')
    telefono = forms.CharField(label='Teléfono', required=False)

    class Meta:
        model = Usuario
        fields = ('correo_claro', 'nombre', 'telefono', 'empresa', 'rol', 'cedula', 'password', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]
