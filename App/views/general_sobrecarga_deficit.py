from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import Count, Q

from App.models.mapa_de_carreras import *


class GeneralSobrecargaDeficitView(TemplateView):
    template_name = 'general_sobrecarga_deficit.html'
    
    def get(self, request):
        #
        docentes = Docente.objects.filter(
            cargo__activo=1, 
            cargo__modalidad__isnull=False, 
            cargo__carga_actual__gt=0
        ).distinct()
        listado = []
        #
        for d in docentes:
            #
            estados_cargos = []
            cargos = Cargo.objects.filter(
                docente=d, 
                activo=1, 
                modalidad__isnull=False, 
                carga_actual__gt=0,
                cargo_cte_ch__isnull=False
            ).distinct()
            #
            for c in cargos:
                #
                estado = ""
                if c.dedicacion.desc_dedic == 'Simple' and c.modalidad.desc_modal == 'Docencia/Desarrollo profesional':
                    if c.carga_actual < 4.0: estado = ("Déficit", "(4,0hs)")
                    elif c.carga_actual > 6.0: estado = ("Sobrecarga", "(6,0hs)")
                #
                elif c.dedicacion.desc_dedic == 'Semided.' and c.modalidad.desc_modal == 'Docencia/Desarrollo profesional':
                    if c.carga_actual < 6.0: estado = ("Déficit", "(6,0hs)")
                    elif c.carga_actual > 10.0: estado = ("Sobrecarga", "(10,0hs)")
                #
                elif c.dedicacion.desc_dedic == 'Semided.' and c.modalidad.desc_modal == 'Docencia e Investigación':
                    if c.carga_actual < 4.0: estado = ("Déficit", "(4,0hs)")
                    elif c.carga_actual > 6.0: estado = ("Sobrecarga", "(6,0hs)")
                #
                elif c.dedicacion.desc_dedic == 'Exclusiva' and c.modalidad.desc_modal == 'Docencia e Investigación':
                    if c.carga_actual < 4.0: estado = ("Déficit", "(4,0hs)")
                    elif c.carga_actual > 8.0: estado = ("Sobrecarga", "(8,0hs)")
                #
                # endfor cargos
                if estado != "": estados_cargos.append({'nro_cargo': c.nro_cargo, 'estado': estado, 'horas': c.carga_actual})
            #
            # endfor docentes
            if estados_cargos: listado.append({'docente': d, 'estados_cargos': estados_cargos})
        #
        # end func
        return render(request, self.template_name, {'docentes': listado})
