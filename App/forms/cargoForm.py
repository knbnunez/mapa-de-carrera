from django import forms
from App.models.mapa_de_carreras import Cargo, Tipo_Extra, Carga_Horaria, Tipo_Extra_CH, Cargo_CTE_CH

class AsignarTareasForm(forms.Form):
    tipo_extra = forms.ModelChoiceField(queryset=None)
    
    cant_horas = forms.IntegerField()  # Campo para el número de horas
    fecha_desde = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Campo para la fecha desde
    fecha_hasta = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Campo para la fecha hasta
  

    cargo = forms.ModelChoiceField(queryset=None)  
    
    def __init__(self, *args, **kwargs):
        tipos_extra = kwargs.pop('tipos_extra')
        
        cargos_activos = kwargs.pop('cargos_activos')  
        
        super().__init__(*args, **kwargs)
        
        self.fields['tipo_extra'].queryset = tipos_extra
        
        self.fields['cargo'].queryset = cargos_activos  # Agrega este queryset

