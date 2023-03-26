from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse
from App.models.mapa_de_carreras import *
import requests
from django.db.models import Q
import json
from requests.exceptions import ConnectTimeout
import datetime


class DocenteTareasView(TemplateView):
    template_name = 'docente_tareas.html'
    username='mapumapa'
    password='Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request, legajo):
        # url = reverse('buscadocente')
        url_buscadocente = self.url_mapuche+'agentes'/{legajo}
        response = requests.get(url_buscadocente, auth=(self.username, self.password))
        # if response.status_code == 200:
        docentes = response.json()
        if Docente.objects.filter(legajo=legajo).exists(): # Existe en la DB UPDATE
                    docente = Docente.objects.get(legajo=legajo)
                    docente.numero_documento = data.get('numero_documento')
                    docente.nombre_apellido  = data.get('agente')
                    docente.save()
      #  print(docentes)
        
        return render(request, self.template_name, {'docentes': docentes})