# app/views.py
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse
from App.models.mapa_de_carreras import *
import requests
from django.db.models import Q
import json
from requests.exceptions import ConnectTimeout
import datetime



class DocenteBusquedaView(TemplateView):
    template_name = 'busca_docente.html'
    username='mapumapa'
    password='Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request):
        url = reverse('buscadocente')
        url_buscadocente = self.url_mapuche+'agentes' # /agentes/{legajo}
        response = requests.get(url_buscadocente, auth=(self.username, self.password))
        # if response.status_code == 200:
        docentes = response.json()
        # print(docentes)
        return render(request, self.template_name, {'docentes': docentes})
        # else :
            # return render(request, self.template_name, {"docentes":})