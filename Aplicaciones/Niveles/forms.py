# forms.py (o en tu vista si preferís mantenerlo ahí)
from django import forms
from ..Header.models import Nivel

class NivelForm(forms.ModelForm):
    class Meta:
        model = Nivel
        fields = ['actividad']
        widgets = {
            'actividad': forms.TextInput(attrs={'class': 'form-control'})
        }
