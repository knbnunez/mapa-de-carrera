# app/views.py
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse
from App.models import *
import requests
from django.db.models import Q
import json
from requests.exceptions import ConnectTimeout


class IndexView(TemplateView):
    template_name = 'index.html' 


class DocenteDetalleView(TemplateView): # Detalle para un único docente
    template_name = 'docente-detalle.html'
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request, legajo): # Se puede recuperar el param atr llamándolo como esta definido en urls.py en este caso: legajo
        # Y no hace falta usar el reverse ni hacer el split
        legajo = str(legajo)
        # print(legajo)
        url_docente = self.url_mapuche+'agentes/'+legajo # /agentes/{legajo}
        url_mail = self.url_mapuche+'agentes/'+legajo+'/mail' # /agentes/{legajo}/mail
        exito = -1
        try:
            responses = [requests.get(url, auth=(self.username, self.password), timeout=5) for url in [url_docente, url_mail]] # timeout = 5 segundos, si no consigue hacer la petición en ese lapso, salta a la excepción
            # exito = -1
            for response in responses:
                if response.status_code == 200:
                    exito += 1
            # Éxito en la consulta            
            if exito == 1: # exito en ambos casos
                jsons = [response.json() for response in responses] # recupero los jsons de las respuestas -> list of jsons
                if not jsons[1]: # En la posición [1] está el correo electrónico, si está vacío lo autocompleto con None
                    jsons[1] = [{'correo_electronico': None}]
                # 1. No existe en la BD -> se crea (create)
                if not Docente.objects.filter(legajo=legajo).exists(): # Caso no existe en la BD
                    # create
                    docente = Docente.objects.create(
                        # numero_documento    = jsons[0]['numero_documento'],
                        numero_documento    = jsons[0].get('numero_documento'), # usar .get() en un dicccionario es equivalente a acceder con ['key'], pero es más seguro porque si no hay nada para esa llave (key), en lugar de lanzar una EXCEPCIÓN, retorno None...
                        legajo              = jsons[0].get('legajo'),
                        nombre_apellido     = jsons[0].get('agente'),
                        correo_electronico  = jsons[1][0].get('correo_electronico') # hay que especificar jsons[idx-lista][idx-lista-attrJson]['attr']
                    )
                    docente.save()
                # 2. Existe en la BD -> se pisan los datos (update)
                else: # Caso sí existe en la BD, lo recupero
                    docente = Docente.objects.get(legajo=legajo)
                    # update all
                    docente.numero_documento    = jsons[0].get('numero_documento')
                    docente.nombre_apellido     = jsons[0].get('agente')
                    docente.correo_electronico  = jsons[1][0].get('correo_electronico')
                    docente.save()
            # Fallo en alguna de las dos consultas agentes o mail
            # else:
                # # 1. No existe en la BD -> algún mensaje en el template sobre que no está cargado
                # if not Docente.objects.filter(legajo=legajo).exists(): # Caso no existe en la BD
                #     docente = None # Luego en el template -> if docente -> muestro; else (docente = None): "no existe"
                # # 2. Existe en la BD -> se muestran los datos de la BD
                # else:
                #     docente = Docente.objects.get(legajo=legajo)
        except ConnectTimeout:
            # if not Docente.objects.filter(legajo=legajo).exists(): docente = None 
            # else: docente = Docente.objects.get(legajo=legajo)
            pass
        # Caso status_code <> 200 para cualquiera de las dos consultas (agentes, mail) y caso excepción ConnectTimeout, junto todo acá
        if exito != 1:   
            # # 1. No existe en la BD -> algún mensaje en el template sobre que el docente no está cargado     
            if not Docente.objects.filter(legajo=legajo).exists(): # Caso no existe en la BD
                docente = None # Luego en el template -> if docente -> muestro; else (docente = None): "no existe"
            # 2. Existe en la BD -> se muestran los datos de la BD
            else:
                docente = Docente.objects.get(legajo=legajo)
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
        # TO DO: Misma lógica que en DocenteDetalle, si hay error en la consulta, etc...
        try:
            response = requests.get(url, auth=(self.username, self.password), timeout=5)
            cargos = response.json()
            # Puede ser útil el codigoescalafon, que nos trae si es DOCE (docente), NODO, AUTO. En teoría el único que nos interesa es DOCE, por lo que capaz nos puede servir para hacer algún control...
            cargos = [{'cargo':_.get('cargo'), 'desc_dedic':_.get('desc_dedic'), 'escalafon':_.get('escalafon')} for _ in response.json()]
            # print(cargos)
            # TO DO: Complejidad, traer la modalidad si hubiera una ya cargada. Cómo llegamos hasta la modalidad cargada para el cargo del docente?
        except ConnectTimeout:
            pass
        return render(request, self.template_name, {'cargos': json.dumps(cargos)})

    # TO DO: almacenar la modalidad y la dedicación que viene en la consulta para la tabla intermedia que genera la restricción de horas + el archivo adjunto

    def post(self, request, legajo):
        
        return self.get(request, legajo) # invoco al método get declarado arriba
