
from django.forms import ModelForm
from .models import Docente
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class criticaForm(ModelForm):
    class Meta:
        model = Docente
        fields = ['legajo']