from django.forms import ModelForm
# from App.models.mapa_de_carreras import Carga_Horaria, Tipo_Extra
from django import forms




class comisionForm(ModelForm):
    
    class Meta:
        # model = Carga_Horaria
        fields = ['cargo','comision', 'fecha_desde', 'fecha_hasta', 'hora_inicio', 'hora_finalizacion']