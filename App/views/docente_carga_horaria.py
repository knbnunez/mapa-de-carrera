# views.py

from App.models.guarani import *
from django.shortcuts import render
from django.views import View
import requests
from django.views.generic import TemplateView
from ..forms.cargaForm import cargaForm
from App.models.mapa_de_carreras import Carga_Horaria, Carrera, Comision, Docente, Materia, Cargo

class DocenteCargaHorariaView(TemplateView):
    template_name = 'docente_carga_horaria.html'
    form_class = cargaForm
    model = Carga_Horaria
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'
     

    def get(self, request):
     
     url_carga = self.url_mapuche+'agentes' # /agentes/{legajo}
     response = requests.get(url_carga, auth=(self.username, self.password))
        # if response.status_code == 200:
     
     docente = response.json()
     
     return render(request, self.template_name, {'docentes': docente})
    
    def get_context_data(self, **kwargs):
     
     context = super().get_context_data(**kwargs)
     comision = Comision.objects.select_related('materia')  # Obtener comisiones con sus materias
     context['comision'] = comision
     context['form'] = self.form_class() 
     return context
    
    
    
    def post(self, request):
        # Obtener el docente y el cargo asociados a los IDs proporcionados
        
        docente = None
        url_carga = self.url_mapuche+'agentes' # /agentes/{legajo}
        response = requests.get(url_carga, auth=(self.username, self.password))
        # if response.status_code == 200:
        docente = response.json() 
     
        comision = Comision.objects.select_related('materia') 
        form = self.form_class(request.POST)
        if form.is_valid():
            # Guardar el formulario si es válido
            carga_extra = form.save(commit=False)
           
            carga_extra.comision = comision 
            carga_extra.save()

        return render(request, 'docente_carga_horaria.html', {'docente': docente,  'comision': comision,'form': form})
