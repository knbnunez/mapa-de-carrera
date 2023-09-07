from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404,render
from App.models.mapa_de_carreras import *
from App.models.guarani import *
# from App.forms.comisionForm import comisionForm
from django.utils import timezone

class DocenteComisionView(TemplateView): # Detalle para un único docente
    template_name = 'docente_comision.html'
    alert = None
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docente = get_object_or_404(Docente, pk=self.kwargs['legajo'])
        cargos = Cargo.objects.filter(docente=docente, activo=1)  # Filtra solo los cargos activos del docente

        current_date = timezone.now().date()
        # print(current_date)

        # Opción más eficiente según chatGpt (spoiler, funciona):
        institutos = Instituto.objects.all()
        carreras_institutos = Carrera_Instituto.objects.select_related('carrera', 'instituto').all()
        # materias_carreras = Materia_Carrera.objects.select_related('materia', 'carrera').all()
        materias_carreras = Materia_Carrera.objects.select_related('materia', 'carrera').filter(materia__comision__comision_ch__carga_horaria__fecha_hasta__gte=current_date).distinct()
        # for mc in materias_carreras: print(mc.materia.nombre)

        comisiones = Comision.objects.filter(comision_ch__carga_horaria__fecha_hasta__gte=current_date).select_related('materia', 'ubicacion').distinct()
        comisiones_ch = Comision_CH.objects.select_related('comision', 'carga_horaria').filter(carga_horaria__fecha_hasta__gte=current_date)
        # for c_ch in comisiones_ch: print(f"id_com: {c_ch.comision} fecha_hasta: {c_ch.carga_horaria.fecha_hasta}")
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
            tipo_dictado = Tipo_Dictado.objects.get(pk=select_tipo_dictado)
            comision_ch = Comision_CH.objects.get(pk=select_comision_ch)
            comision_ch.tipo_dictado = tipo_dictado
            comision_ch.save()
            comision_cte_ch, _ = Cargo_CTE_CH.objects.get_or_create(cargo=cargo, comision_ch=comision_ch, tipo_extra_ch=None)
            DocenteComisionView.alert = None
        except (Cargo.DoesNotExist, Comision_CH.DoesNotExist):
            DocenteComisionView.alert = "El Cargo, la Comision o la Franja Horaria estaban vacíos o mal cargados!"
        return self.get(request, legajo)