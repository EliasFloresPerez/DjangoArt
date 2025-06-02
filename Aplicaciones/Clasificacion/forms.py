from django import forms
from ..Header.models import Clasificacion
from ..Header.models import Nivel


class ClasificacionForm(forms.ModelForm):
    class Meta:
        model = Clasificacion
        fields = ['cod_actividad', 'descripcion', 'nivel']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Excluir nivel con id=1
        self.fields['nivel'].queryset = Nivel.objects.exclude(id=1)
