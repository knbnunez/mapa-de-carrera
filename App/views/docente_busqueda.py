from django.views.generic import TemplateView
from django.shortcuts import render
from App.models.mapa_de_carreras import *
import requests
from requests.exceptions import ConnectTimeout


class DocenteBusquedaView(TemplateView):
    template_name = 'docente_busqueda.html'

    def get(self, request):
        docentes = Docente.objects.all()
        return render(request, self.template_name, {'docentes': docentes})