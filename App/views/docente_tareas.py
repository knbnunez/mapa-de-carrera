from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404,render
from django.http import JsonResponse
from requests.exceptions import ConnectTimeout
import datetime
from App.models.mapa_de_carreras import *
from App.models.guarani import *
from App.forms.cargoForm import cargoForm

class DocenteTareasView(TemplateView): # Detalle para un único docente
    template_name = 'docente_tareas.html'
    form_class = cargoForm
    # model = Carga_Horaria
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'
     


    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     docente = get_object_or_404(Docente, pk=self.kwargs['legajo'])
     cargos = Cargo.objects.filter(docente=docente, activo=1) 
     #cargo = get_object_or_404(Cargo, pk=self.kwargs['nro_cargo'], docente=docente)
     context['docente'] = docente
     context['cargo'] = cargos
    # context['form'] = self.form_class() 
     return context
    
    
    def post(self, request, legajo):
        # Obtener el docente y el cargo asociados a los IDs proporcionados
        docente = get_object_or_404(Docente, pk=legajo)
        cargos = Cargo.objects.filter(docente=docente, activo=1) 
        #cargo = get_object_or_404(Cargo, pk=nro_cargo, docente=docente)
        
        form = self.form_class(request.POST)
        if form.is_valid():
            # Guardar el formulario si es válido
            carga_extra = form.save(commit=False)
            #  carga_extra.cargo = cargos
            carga_extra.save()

        return render(request, 'docente_tareas.html', {'docente': docente, 'cargo': cargos, 'form': form})