from django import forms
from .models import Cita

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['Id_paciente', 'Id_doctor', 'fecha_limite']
        widgets = {
            'fecha_limite': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
