from django.forms import ModelForm
from App.models.mapa_de_carreras import Carga_Horaria, Tipo_Extra
from django import forms




class cargoForm(ModelForm):
    tipo_extra = forms.ModelChoiceField(queryset=Tipo_Extra.objects.all(), required=False)

    class Meta:
        model = Carga_Horaria
        fields = ['cargo', 'comision', 'tipo_extra', 'fecha_desde', 'fecha_hasta', 'hora_inicio', 'hora_finalizacion']