
# app/views.py
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse
from App.models import *
import requests


class IndexView(TemplateView):
    template_name = 'index.html' #your_template


class DocenteView(TemplateView):
    template_name = 'docente.html'
    username='mapa'
    password='gobenoz77'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request, legajo):
        url = reverse('docente', kwargs={'legajo': legajo})
        recover_legajo = url.split('/')[-2] # split('/') = ['', 'game', 'id', '']; split('/')[-2] = ['id']
        if Docente.objects.filter(legajo=recover_legajo).exists():
            docente = Docente.objects.get(legajo=recover_legajo)
        else: 
            url = self.url_mapuche+'agentes/'+recover_legajo
            print({'url': url})
            response = requests.get(url, auth=(self.username, self.password))
            json_docente = response.json()
            print({'json_docente': json_docente})
            url = self.url_mapuche+'agentes/'+recover_legajo+'/mail'
            print({'url': url})
            response = requests.get(url, auth=(self.username, self.password))
            json_mail = response.json()
            print({'json_mail': json_mail})
            docente = Docente(
                dni=json_docente['numero_documento'],
                legajo=json_docente['legajo'],
                nombre_apellido=json_docente['agente'],
                fecha_ingreso=json_docente['fecha_ingreso'],
                fecha_jubilacion=json_docente['fecha_jubilacion'],
                mail=json_mail['correo_electronico']
            )
            docente.save()
            print({'docente': docente})
        return render(requests, self.template_name, { 'docente': docente})