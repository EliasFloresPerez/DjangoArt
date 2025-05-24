from django import forms
from ..Header.models import Empresa


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nombre', 
            'actividad_economica', 
            'razon_social', 
            'representante', 
            'telefono', 
            'ruc', 
            'clasificacion',
            'ciudad',
            'provincia'
        ]