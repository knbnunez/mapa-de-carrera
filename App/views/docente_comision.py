from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404,render
from django.http import JsonResponse
from requests.exceptions import ConnectTimeout
import datetime
from App.models.mapa_de_carreras import *
from App.models.guarani import *
from App.forms.comisionForm import comisionForm

class DocenteComisionView(TemplateView): # Detalle para un único docente
    template_name = 'docente_comision.html'
    form_class = comisionForm
    # model = Carga_Horaria
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'
     


    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     docente = get_object_or_404(Docente, pk=self.kwargs['legajo'])
     cargos = Cargo.objects.filter(docente=docente, activo=1)  # Filtra solo los cargos activos del docente
     comisiones = Comision.objects.select_related('materia')  # Obtener comisiones con sus materias
    #  fecha_desde = SgaComisionesBH.objects.filter(comision=comisiones) 

    # ToDo: asignaciones: fecha_desde,, fecha_hasta, hora_inicio, hora_fin

     context['docente'] = docente
     context['cargo'] = cargos
     context['comision'] = comisiones
    #  context['fecha_desde'] = fecha_desde
     context['form'] = self.form_class() 
     return context
    
    
    def post(self, request, legajo):
        # Obtener el docente y el cargo asociados a los IDs proporcionados
        docente = get_object_or_404(Docente, pk=legajo)
        cargos = Cargo.objects.filter(docente=docente, activo=1) 
        comisiones = Comision.objects.select_related('materia') 
        # fecha_desde = SgaComisionesBH.objects.all() 
        form = self.form_class(request.POST)
        if form.is_valid():
            # Guardar el formulario si es válido
            carga_extra = form.save(commit=False)
            #carga_extra.cargo = cargos
            #carga_extra.comision = comisiones 
            carga_extra.save()

        return render(request, 'docente_comision.html', {
           'docente': docente, 
           'cargo': cargos, 
        #    'fecha_desde': fecha_desde,
           'comisiones': comisiones,
           'form': form})