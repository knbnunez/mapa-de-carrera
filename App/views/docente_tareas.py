from pyexpat.errors import messages
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect,render
from django.http import HttpResponse, JsonResponse
from requests.exceptions import ConnectTimeout
import datetime
from App.models.mapa_de_carreras import *
from App.models.guarani import *
from App.forms.cargoForm import  AsignarTareasForm

class DocenteTareasView(TemplateView): # Detalle para un único docente
    template_name = 'docente_tareas.html'
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'
     


    def get(self, request, legajo):
        docente = get_object_or_404(Docente, legajo=legajo)
        cargos_activos = Cargo.objects.filter(docente=docente, activo=1)
        tipos_extra = Tipo_Extra.objects.all()
        
        
        form = AsignarTareasForm(
            tipos_extra=tipos_extra,
            
            cargos_activos=cargos_activos  # Agrega esto para pasar los cargos al formulario
        )
        
        context = {
            'docente': docente,
            'form': form,
        }
        return render(request, self.template_name, context)
    

    def post(self, request, legajo):
        docente = get_object_or_404(Docente, legajo=legajo)
        form = AsignarTareasForm(
            request.POST,
            tipos_extra=Tipo_Extra.objects.all(),
            cargos_activos=Cargo.objects.filter(docente=docente, activo=1)
        )
        
        if form.is_valid():
            tipo_extra = form.cleaned_data['tipo_extra']
            cargo = form.cleaned_data['cargo']  # Obtener el cargo seleccionado del formulario
            cant_horas = form.cleaned_data['cant_horas']
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            
            # Guardar en Tipo_Extra_CH
            tipo_extra_ch = Tipo_Extra_CH.objects.create(
                
                tipo_extra=tipo_extra,
                cant_horas=cant_horas,
                fecha_desde=fecha_desde,
                fecha_hasta=fecha_hasta,
            )
            
            # Guardar en Cargo_CTE_CH
            cargo_cte_ch = Cargo_CTE_CH.objects.create(
             cargo=cargo,
             tipo_extra_ch=tipo_extra_ch,
         )
           
            
        
        context = {
            'docente': docente,
            'form': form,
        }
        return render(request, self.template_name, context)

