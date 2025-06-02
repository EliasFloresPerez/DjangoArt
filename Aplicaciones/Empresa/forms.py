from django import forms
from ..Header.models import Empresa
from ..Header.models import Clasificacion

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Excluir clasificacion con id=1 del campo clasificacion
        self.fields['clasificacion'].queryset = Clasificacion.objects.exclude(id=1)