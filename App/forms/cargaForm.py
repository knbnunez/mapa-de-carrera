from django import forms
# from App.models.mapa_de_carreras import Carga_Horaria, Docente

class cargaForm(forms.Form):
    class Meta:
        # model = Carga_Horaria
        fields = ['comision', 'fecha_desde', 'fecha_hasta', 'hora_inicio', 'hora_finalizacion']
