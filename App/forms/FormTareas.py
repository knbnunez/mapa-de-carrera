from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from App.models.mapa_de_carreras import Carga_Horaria

class FormTareas(ModelForm):
    class Meta:
        model = Carga_Horaria
        fields = ['tipo_extra']