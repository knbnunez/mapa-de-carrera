from django import forms
from App.models.mapa_de_carreras  import Comision, Docente

class ComisionDocenteForm(forms.Form):
    comision_materia = forms.ModelChoiceField(queryset=Comision.objects.all(), label='Comisión y Materia')
    docente_legajo_nombre = forms.ModelChoiceField(queryset=Docente.objects.all(), label='Docente (Legajo - Nombre)')