
from django import forms
from ..Header.models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['codigo', 'descripcion']

