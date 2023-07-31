from django import forms
from App.models.mapa_de_carreras  import Instituto, Carrera, Materia, Comision, Docente

class AsignarDocenteForm(forms.Form):
    instituto = forms.ModelChoiceField(queryset=Instituto.objects.all(), label='Instituto')
    carrera = forms.ModelChoiceField(queryset=Carrera.objects.none(), label='Carrera', required=False)
    materia = forms.ModelChoiceField(queryset=Materia.objects.none(), label='Materia', required=False)
    comision = forms.ModelChoiceField(queryset=Comision.objects.none(), label='Comisión', required=False)
    docente = forms.ModelChoiceField(queryset=Docente.objects.none(), label='Docente', required=False)