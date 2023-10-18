from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404,render
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField

from App.models.mapa_de_carreras import *
from App.models.guarani import *
from App.functions import calcular_horas

class DocenteComisionView(TemplateView): # Detalle para un único docente
    template_name = 'docente_comision.html'
    alert = None
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docente = get_object_or_404(Docente, pk=self.kwargs['legajo'])
        cargos = Cargo.objects.filter(docente=docente, activo=1)  # Filtra solo los cargos activos del docente

        current_date = timezone.now().date()

        # Opción más eficiente según chatGpt (spoiler, funciona):
        institutos = Instituto.objects.all().order_by('nombre')
        carreras_institutos = Carrera_Instituto.objects.select_related('carrera', 'instituto').all().order_by('carrera__nombre')
        materias_carreras = Materia_Carrera.objects.select_related('materia', 'carrera').filter(materia__comision__comision_ch__carga_horaria__fecha_hasta__gte=current_date).distinct().order_by('materia__nombre')

        comisiones = Comision.objects.filter(comision_ch__carga_horaria__fecha_hasta__gte=current_date).select_related('materia', 'ubicacion').distinct()

        comisiones_ch = Comision_CH.objects.select_related('comision', 'carga_horaria').filter(
            carga_horaria__fecha_hasta__gte=current_date
        ).annotate(
            dia_semana_order=Case(
                When(carga_horaria__dia_semana='Lunes', then=Value(1)),
                When(carga_horaria__dia_semana='Martes', then=Value(2)),
                When(carga_horaria__dia_semana='Miercoles', then=Value(3)),
                When(carga_horaria__dia_semana='Jueves', then=Value(4)),
                When(carga_horaria__dia_semana='Viernes', then=Value(5)),
                default=Value(6), output_field=IntegerField()
            )
).order_by('dia_semana_order')

        tipos_dictados = Tipo_Dictado.objects.all()

        context['docente'] = docente
        context['cargos'] = cargos
        context['institutos'] = institutos
        context['carreras_institutos'] = carreras_institutos
        context['materias_carreras'] = materias_carreras
        context['comisiones'] = comisiones
        context['comisiones_ch'] = comisiones_ch
        context['tipos_dictados'] = tipos_dictados
        context['alert'] = DocenteComisionView.alert
        return context
    
    
    def post(self, request, legajo):
        select_cargo = request.POST.get('select-cargo')
        select_comision_ch = request.POST.get('select-comision_ch')
        select_tipo_dictado = request.POST.get('select-tipo_dictado')
       
        try:
            cargo = Cargo.objects.get(nro_cargo=select_cargo)
            comision_ch = Comision_CH.objects.get(pk=select_comision_ch)
            tipo_dictado = Tipo_Dictado.objects.get(pk=select_tipo_dictado)
            comision_ch.tipo_dictado = tipo_dictado
            comision_ch.save()
            Cargo_CTE_CH.objects.get_or_create(cargo=cargo, comision_ch=comision_ch, tipo_extra_ch=None) # no me interesa recuperarlo en realidad, si devuelve por el 'get', lo descarto, es un simple control para que no se generen duplicados
            calcular_horas(legajo)

            DocenteComisionView.alert = None
        except (Cargo.DoesNotExist, Comision_CH.DoesNotExist):
            DocenteComisionView.alert = "El Cargo, la Comision o la Franja Horaria estaban vacíos o mal cargados!"
        
        # End def
        return self.get(request, legajo)