from django.views.generic import TemplateView
from django.shortcuts import render
from App.models.mapa_de_carreras import *
import requests
from requests.exceptions import ConnectTimeout


class DocenteBusquedaView(TemplateView):
    template_name = 'docente_busqueda.html'
    username='mapumapa'
    password='Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request):
        try:
            url_buscadocente = self.url_mapuche+'agentes' # /agentes
            response = requests.get(url_buscadocente, auth=(self.username, self.password), timeout=5)

            if response.status_code == 200:
                docentes = response.json() # json() convierte a diccionario de python    
                
                # Recuperar escalafón 'docentes'
                aux = []
                for d in docentes:
                    cargos = requests.get(url_buscadocente+f"/{d['legajo']}/cargos", auth=(self.username, self.password)).json()
                    es_docente = False
                    for c in cargos:
                        if('nodo' not in c['escalafon'].lower().replace(" ", "")): # Con esta normalización de texto, cualquier escalafon <> a 'nodo' (no docente) es considera docente
                            es_docente = True
                            break # Salgo del bucle
                    if(es_docente): aux.append(d)

                docentes = aux # Almacenamos todos los 'docentes' recuperados
            
            else: # status_code <> 200 --> Error --> Busco los datos de la base
                docentes = Docente.objects.all() # Puede devolver vacío

        except ConnectTimeout: pass # timeout 5' --> Error
        
        return render(request, self.template_name, {'docentes': docentes})