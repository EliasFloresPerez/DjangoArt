from django import forms
from ..Header.models import Clasificacion

class ClasificacionForm(forms.ModelForm):
    class Meta:
        model = Clasificacion
        fields = ['cod_actividad', 'descripcion', 'nivel']
