from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404,render
from django.http import JsonResponse
from requests.exceptions import ConnectTimeout
import datetime
from App.models.mapa_de_carreras import *
from App.models.guarani import *
from App.cargoForm import cargoForm

class DocenteTareasView(TemplateView): # Detalle para un único docente
    template_name = 'docente_tareas.html'
    form_class = cargoForm
    model = Carga_Horaria
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'
     


    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     docente = get_object_or_404(Docente, pk=self.kwargs['legajo'])
     cargo = get_object_or_404(Cargo, pk=self.kwargs['nro_cargo'], docente=docente)
     context['docente'] = docente
     context['cargo'] = cargo
     context['form'] = self.form_class() 
     return context
    
    
    def post(self, request, legajo, nro_cargo):
        # Obtener el docente y el cargo asociados a los IDs proporcionados
        docente = get_object_or_404(Docente, pk=legajo)
        cargo = get_object_or_404(Cargo, pk=nro_cargo, docente=docente)

        form = self.form_class(request.POST)
        if form.is_valid():
            # Guardar el formulario si es válido
            carga_extra = form.save(commit=False)
            carga_extra.cargo = cargo
            carga_extra.save()

        return render(request, 'docente_tareas.html', {'docente': docente, 'cargo': cargo, 'form': form})

    #def post(self, request, legajo, nro_cargo):
        # Obtener el docente y el cargo asociados a los IDs proporcionados
     #   docente = get_object_or_404(Docente, pk=legajo)
      #  cargo = get_object_or_404(Cargo, pk=nro_cargo, docente=docente)

        # Obtener los datos del formulario enviado por el cliente
      #  fecha_desde = request.POST.get('fecha_desde')
      #  fecha_hasta = request.POST.get('fecha_hasta')
     #   hora_inicio = request.POST.get('hora_inicio')
     #   hora_finalizacion = request.POST.get('hora_finalizacion')

        # Crear la carga horaria extra
       # carga_extra = Carga_Horaria(
        #  #  cargo=cargo,
           # Tipo_Extra=Tipo_Extra,
         #   fecha_desde=fecha_desde,
        # #   fecha_hasta=fecha_hasta,
       # #    hora_inicio=hora_inicio,
      # #     hora_finalizacion=hora_finalizacion
      ##  )
      #  carga_extra.save()

        # Si deseas devolver una respuesta JSON indicando el éxito de la operación
        
      #  return render(request, 'docente_tareas.html', {'docente': docente, 'cargo': cargo})
