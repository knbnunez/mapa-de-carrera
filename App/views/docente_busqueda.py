from django.views.generic import TemplateView

from django.shortcuts import render
from django.urls import reverse
from App.models.mapa_de_carreras import *
import requests
from django.db.models import Q
import json
from requests.exceptions import ConnectTimeout
import datetime

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
# app/views.py
class DocenteBusquedaView(TemplateView):
    template_name = 'docente_busqueda.html'
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
    def busca(request):
       # url=self.url_mapuche+'agentes/'+legajo
        queryset = request.Get.get('q')
        if queryset:
            docentes = Docente.objects.filter(legajo=queryset).first()
            if docentes:
                url = reverse('docente-detalle', kwargs={'legajo':queryset})
              #  return redirect('docentes', legajo=queryset)
     #    if queryset:
      #         docentes = Post.objects.filter(
      #             Q(legajo = queryset) 
      #         )
      #   responses = [requests.get(url, auth=(self.username, self.password), timeout=5) for url in [url]]
      #  return render(request, 'docente-detalle.html', {'docentes': json.dumps(docentes),'queryset':queryset} )
        return render(request, 'docente_detalle.html', {'queryset':queryset} )
