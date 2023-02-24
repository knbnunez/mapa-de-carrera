
# app/views.py
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse
from App.models import *
import requests
from django.db.models import Q


class IndexView(TemplateView):
    template_name = 'index.html' #your_template


class DocenteView(TemplateView):
    template_name = 'docente.html'
    username='mapumapa'
    password='Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request, legajo):
        url = reverse('docente', kwargs={'legajo': legajo})
        recover_legajo = url.split('/')[-2] # split('/') = ['', 'game', 'id', '']; split('/')[-2] = ['id']
        url_docente = self.url_mapuche+'agentes/'+recover_legajo # /agentes/{legajo}
        url_mail = self.url_mapuche+'agentes/'+recover_legajo+'/mail' # /agentes/{legajo}/mail
        # responses[0] = requests.get(url_docente, auth=(self.username, self.password))
        # responses[1] = requests.get(url_mail, auth=(self.username, self.password))
        responses = [requests.get(url, auth=(self.username, self.password)) for url in [url_docente, url_mail]] # lo mismo, pero hecho con lista por comprensión
        exito = -1
        for response in responses:
            if response.status_code == 200:
                exito += 1
        if exito == 1: # exito en ambos casos
            jsons = [response.json() for response in responses]
            # for json in jsons:
            #     print(json)
            if not jsons[1]: # Consulto si la lista en la posición [1] está vacía
                jsons[1] = [{'correo_electronico': None}]
            if jsons[0]['fecha_jubilacion'] is 'null':
                jsons[0]['fecha_jubilacion'] = None
            # else: no está vacío y no hay que hacer nada, ya tiene un valor
            docente = Docente(
                numero_documento    = jsons[0]['numero_documento'],
                legajo              = jsons[0]['legajo'],
                nombre_apellido     = jsons[0]['agente'],
                fecha_ingreso       = jsons[0]['fecha_ingreso'],
                fecha_jubilacion    = jsons[0]['fecha_jubilacion'],     # jsons[idx-lista]['attr']
                correo_electronico  = jsons[1][0]['correo_electronico'] # hay que especificar jsons[idx-lista][idx-lista-attrJson]['attr']
            )
            # TO DO: guardarlo en la base de datos. docente.save() y algo más?

        # TO DO: else
        return render(request, self.template_name, { 'docente': docente})



class DocenteBusquedaView(TemplateView):
    template_name = 'buscadocente.html'
    username='mapumapa'
    password='Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request):
        url = reverse('buscadocente')
        #recover_legajo = url.split('/')[-2] # split('/') = ['', 'game', 'id', '']; split('/')[-2] = ['id']
        url_buscadocente = self.url_mapuche+'agentes' # /agentes/{legajo}
        
        # responses[0] = requests.get(url_docente, auth=(self.username, self.password))
        # responses[1] = requests.get(url_mail, auth=(self.username, self.password))
        response = requests.get(url_buscadocente, auth=(self.username, self.password))
        #if response.status_code == 200:
                      
        docentes= response.json()

        print (docentes)
        return render(request, self.template_name, {"docentes":docentes})
        
       # else :
        #    return render(request, self.template_name, {"docentes":})
    # def get_buscar (request):
      #   queryset = request.GET.get("buscar")
        # posts=Post.objects.filter(estado = True)
         #if queryset:
           #  posts =Post.objects.filter(
             #    Q(legajo = queryset)

             #)
         #return render (request,'docente.html',('posts':posts)) 