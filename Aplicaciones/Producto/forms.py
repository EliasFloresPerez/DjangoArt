from django import forms
from ..Header.models import Producto

class ProductoForm(forms.ModelForm):
    ESTADOS_PRODUCTO = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
        ('Malo', 'Malo'),
        ('En reparación', 'En reparación'),
        ('Dañado', 'Dañado'),
    ]

    estado = forms.ChoiceField(choices=ESTADOS_PRODUCTO)

    class Meta:
        model = Producto
        fields = [
            'codigo', 'categoria', 'peso', 'estado', 'empresa',
            'nombre', 'cantidad', 'origen', 'descripcion', 'fecha_ingreso'
        ]
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Empresa no es requerida en el formulario
        self.fields['empresa'].required = False
