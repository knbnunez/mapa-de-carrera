from django.views.generic import TemplateView
from django.shortcuts import render
from App.models.mapa_de_carreras import *
import requests
import json
from requests.exceptions import ConnectTimeout


class DocenteModalidadView(TemplateView):
    template_name = 'docente_modalidad.html'
    username = 'mapumapa'
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request, legajo):
        legajo = str(legajo) 
        # NOTA:
        # CONSIDERAMOS QUE: SI YA PASARON POR LA PANTALLA DE DETALLE-DOCENTE PARA LLEGAR HASTA ACÁ, SIGNIFICA QUE YA SE ACTUALIZARON LOS DATOS QUE ESTABAN EN LA BASE, ASÍ QUE LOS PODEMOS CONSUMIR DIRECTAMENTE
        docente = Docente.objects.get(legajo=legajo)
        # cargo = Cargo.objects.get(docente=docente).filter(activo=1) 

        return render(request, self.template_name)

    # TO DO: almacenar la modalidad y la dedicación que viene en la consulta para la tabla intermedia que genera la restricción de horas + el archivo adjunto

    def post(self, request, legajo):
        
        return self.get(request, legajo) # invoco al método get declarado arriba