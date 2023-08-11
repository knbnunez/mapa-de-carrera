from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404,render
from App.models.mapa_de_carreras import *
from App.models.guarani import *
# from App.forms.comisionForm import comisionForm

class DocenteComisionView(TemplateView): # Detalle para un único docente
    template_name = 'docente_comision.html'
    # form_class = comisionForm
    # model = Carga_Horaria
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docente = get_object_or_404(Docente, pk=self.kwargs['legajo'])
        cargos = Cargo.objects.filter(docente=docente, activo=1)  # Filtra solo los cargos activos del docente
        # comisiones = Comision.objects.select_related('materia')  # Obtener comisiones con sus materias
        #  fecha_desde = SgaComisionesBH.objects.filter(comision=comisiones) 

        # institutos = Instituto.objects.all()
        # carreras_institutos = Carrera_Instituto.objects.all()
        # materias_carreras = Materia_Carrera.objects.all()
        # comisiones = Comision.objects.all()

        # Opción más eficiente según chatGpt (spoiler, funciona):
        institutos = Instituto.objects.all()
        carreras_institutos = Carrera_Instituto.objects.select_related('carrera', 'instituto').all()
        materias_carreras = Materia_Carrera.objects.select_related('materia', 'carrera').all()
        comisiones = Comision.objects.select_related('materia', 'ubicacion').all()
        comisiones_ch = Comision_CH.objects.select_related('comision', 'carga_horaria').all()
        # print(comisiones_ch)

        # ToDo: asignaciones: fecha_desde, fecha_hasta, hora_inicio, hora_fin

        context['docente'] = docente
        context['cargos'] = cargos
        context['institutos'] = institutos
        context['carreras_institutos'] = carreras_institutos
        context['materias_carreras'] = materias_carreras
        context['comisiones'] = comisiones
        context['comisiones_ch'] = comisiones_ch

        # for comision in comisiones:
        #     print(comision)
        
        # for instituto in institutos:
        #     print(instituto)

        # print(institutos)

        #  context['fecha_desde'] = fecha_desde
        # context['form'] = self.form_class()
        # print("Termino de traer los datos súper rápido, qué es lo que tarda?, es del lado del cliente") 
        return context
    
    
    def post(self, request, legajo):
        select_cargo = request.POST.get('select-cargo')
        # print(select_cargo)
        select_comision_ch = request.POST.get('select-comision_ch')
        # print(select_comision_ch)

        # ToDo comprobar que sea correcta la combinación de inputs elegidos, instituto - carrera - materia - comisión - franja horaria

        cargo = Cargo.objects.get(nro_cargo=select_cargo)
        comision_ch = Comision_CH.objects.get(pk=select_comision_ch)
        
        comision_cte_ch, _ = Cargo_CTE_CH.objects.get_or_create(
            cargo=cargo,
            comision_ch=comision_ch,
            tipo_extra_ch=None
        )
        return self.get(request, legajo)

        