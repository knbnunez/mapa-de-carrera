
# forms.py

from django import forms
from App.models.mapa_de_carreras import Cargo, Tipo_Extra, Carga_Horaria, Tipo_Extra_CH, Cargo_CTE_CH

class AsignarTareasForm(forms.Form):
    tipo_extra = forms.ModelChoiceField(queryset=None)
    carga_horaria = forms.ModelChoiceField(queryset=None)
    cargo = forms.ModelChoiceField(queryset=None)  # Agrega este campo
    
    def __init__(self, *args, **kwargs):
        tipos_extra = kwargs.pop('tipos_extra')
        carga_horaria = kwargs.pop('carga_horaria')
        cargos_activos = kwargs.pop('cargos_activos')  # Agrega esto
        
        super().__init__(*args, **kwargs)
        
        self.fields['tipo_extra'].queryset = tipos_extra
        self.fields['carga_horaria'].queryset = carga_horaria
        self.fields['cargo'].queryset = cargos_activos  # Agrega este queryset



class AsignarCargaHorariaForm(forms.Form):
    carga_horaria = forms.ModelChoiceField(queryset=None)
    
    def __init__(self, *args, **kwargs):
        carga_horaria = kwargs.pop('carga_horaria')
        
        super().__init__(*args, **kwargs)
        
        self.fields['carga_horaria'].queryset = carga_horaria
