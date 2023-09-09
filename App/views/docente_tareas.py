from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from App.models.mapa_de_carreras import *
from App.models.guarani import *
from App.forms.cargoForm import AsignarTareasForm

class DocenteTareasView(TemplateView):
    template_name = 'docente_tareas.html'

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
            # Verificar si todos los campos requeridos tienen datos
            if (
                form.cleaned_data.get('tipo_extra') is not None and
                form.cleaned_data.get('cargo') is not None and
                form.cleaned_data.get('cant_horas') is not None and
                form.cleaned_data.get('fecha_desde') is not None and
                form.cleaned_data.get('fecha_hasta') is not None
            ):
                # Una vez verificado que existen datos cargados, se procede a recuperarlos
                tipo_extra = form.cleaned_data['tipo_extra']
                cargo = form.cleaned_data['cargo'] 
                cant_horas = form.cleaned_data['cant_horas']
                fecha_desde = form.cleaned_data['fecha_desde']
                fecha_hasta = form.cleaned_data['fecha_hasta']
                
                if cant_horas > 0 and cant_horas <= 999:
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