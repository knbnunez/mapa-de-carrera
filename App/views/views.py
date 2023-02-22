
# app/views.py
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse
from App.models import *
import requests
import json


class IndexView(TemplateView):
    template_name = 'index.html' 


class DetalleDocenteView(TemplateView): # Detalle para un único docente
    template_name = 'docente.html'
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request, legajo): # Se puede recuperar el param atr llamándolo como esta definido en urls.py en este caso: legajo
        # Y no hace falta usar el reverse ni hacer el split
        legajo = str(legajo)
        # print(legajo)
        url_docente = self.url_mapuche+'agentes/'+legajo # /agentes/{legajo}
        url_mail = self.url_mapuche+'agentes/'+legajo+'/mail' # /agentes/{legajo}/mail
        responses = [requests.get(url, auth=(self.username, self.password)) for url in [url_docente, url_mail]] # lo mismo, pero hecho con lista por comprensión
        exito = -1
        for response in responses:
            if response.status_code == 200:
                exito += 1

        # Éxito en la consulta
            # 1. No existe en la BD -> se crea (create)
            # 2. Existe en la BD -> se pisan los datos (update)
        if exito == 1: # exito en ambos casos
            jsons = [response.json() for response in responses]
            if not jsons[1]: # Consulto si la lista en la posición [1] está vacía
                jsons[1] = [{'correo_electronico': None}]
            # if jsons[0]['fecha_jubilacion'] is 'null':
            #     jsons[0]['fecha_jubilacion'] = None
            
            
            # TODO: consultas a la BD ejemplo
            # if not Game.objects.filter(id=recover_id).exists(): # not exists?? 
                # game = Game.objects.get(id=recover_id)
            # else: 

            docente = Docente(
                # numero_documento    = jsons[0]['numero_documento'],
                numero_documento    = jsons[0].get('numero_documento'), # usar .get() en un dicccionario es equivalente a acceder con ['key'], pero es más seguro porque si no hay nada para esa llave (key), en lugar de lanzar una EXCEPCIÓN, retorno None...
                legajo              = jsons[0].get('legajo'),
                nombre_apellido     = jsons[0].get('agente'),
                fecha_ingreso       = jsons[0].get('fecha_ingreso'),
                fecha_jubilacion    = jsons[0].get('fecha_jubilacion'),     # jsons[idx-lista]['attr']
                correo_electronico  = jsons[1][0].get('correo_electronico') # hay que especificar jsons[idx-lista][idx-lista-attrJson]['attr']
            )
            # TO DO: guardarlo en la base de datos. docente.save() y algo más?

        # TO DO: else (es un status_code <> 200):
            # 1. No existe en la BD -> algún mensaje en el template sobre que no está cargado
            # 2. Existe en la BD -> se muestran los datos de la BD

        return render(request, self.template_name, {'docente': docente})


class DocenteBusquedaView(TemplateView):
    template_name = 'buscadocente.html'
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


class DocenteModalidadView(TemplateView):
    template_name = 'docente-modalidad.html'
    username = 'mapumapa'
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request, legajo):
        legajo = str(legajo) 
        url = self.url_mapuche+'agentes/'+legajo+'/cargos' # /agentes/{legajo}/cargos
        response = requests.get(url, auth=(self.username, self.password))
        cargos = response.json()
        cargos = [{'cargo':_.get('cargo'), 'desc_categ':_.get('desc_categ'), 'desc_dedic':_.get('desc_dedic')} for _ in response.json()]
        # print(cargos)
        # TO DO: si hay modalidad cargada, recuperarla desde la DB
        return render(request, self.template_name, {'cargos': json.dumps(cargos)})

    # TO DO: almacenar la modalidad y la dedicación que viene en la consulta para la tabla intermedia que genera la restricción de horas + el archivo adjunto
    def post(self, request, legajo):
        
        return self.get(request, legajo) # invoco al método get declarado arriba