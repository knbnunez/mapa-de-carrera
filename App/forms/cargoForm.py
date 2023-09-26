from django import forms
from App.models.mapa_de_carreras import Cargo, Tipo_Extra, Carga_Horaria, Tipo_Extra_CH, Cargo_CTE_CH

class AsignarTareasForm(forms.Form):
    cargo = forms.ModelChoiceField(queryset=None)  
    tipo_extra = forms.ModelChoiceField(queryset=None)
    cant_horas = forms.FloatField(
        initial=0,
        widget=forms.TextInput(attrs={'class': 'rounded-lg h-[30.5px] sm:w-full w-12 text-sm font-semibold'})
    )
    fecha_desde = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'rounded-lg h-8 w-full text-sm font-semibold'
    }))
    fecha_hasta = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'rounded-lg h-8 w-full text-sm font-semibold'
    }))
    
    def __init__(self, *args, **kwargs):
        tipos_extra = kwargs.pop('tipos_extra')
        cargos_activos = kwargs.pop('cargos_activos')  
        super().__init__(*args, **kwargs)
        self.fields['tipo_extra'].queryset = tipos_extra
        self.fields['cargo'].queryset = cargos_activos 