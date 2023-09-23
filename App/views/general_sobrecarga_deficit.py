from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import Count, Q

from App.models.mapa_de_carreras import *


class GeneralSobrecargaDeficitView(TemplateView):
    template_name = 'general_sobrecarga_deficit.html'
    
    def get(self, request):
        print("Hola?")
        #
        docentes = Docente.objects.filter(
            cargo__activo=1, 
            cargo__modalidad__isnull=False, 
            cargo__carga_actual__gt=0
        ).distinct()
        print(docentes)
        listado = []
        #
        for d in docentes:
            print(d)
            #
            estados_cargos = []
            cargos = Cargo.objects.filter(
                docente=d, 
                activo=1, 
                modalidad__isnull=False, 
                carga_actual__gt=0
            )
            #
            for c in cargos:
                print(c)
                #
                estado = ""
                if c.dedicacion.desc_dedic == 'Simple' and c.modalidad.desc_modal == 'Docencia/Desarrollo profesional':
                    if c.carga_actual < 4.0: estado = "Déficit"
                    elif c.carga_actual > 6.0: estado = "Sobrecarga"
                #
                elif c.dedicacion.desc_dedic == 'Semided.' and c.modalidad.desc_modal == 'Docencia/Desarrollo profesional':
                    if c.carga_actual < 6.0: estado = "Déficit"
                    elif c.carga_actual > 10.0: estado = "Sobrecarga"
                #
                elif c.dedicacion.desc_dedic == 'Semided.' and c.modalidad.desc_modal == 'Docencia e Investigación':
                    if c.carga_actual < 4.0: estado = "Déficit"
                    elif c.carga_actual > 6.0: estado = "Sobrecarga"
                #
                elif c.dedicacion.desc_dedic == 'Exclusiva' and c.modalidad.desc_modal == 'Docencia e Investigación':
                    if c.carga_actual < 4.0: estado = "Déficit"
                    elif c.carga_actual > 8.0: estado = "Sobrecarga"
                #
                # endfor cargos
                if estado != "": estados_cargos.append({'nro_cargo': c.nro_cargo, 'estado': estado, 'horas': c.carga_actual})
            #
            # endfor docentes
            if estados_cargos: listado.append({'docente': d, 'estados_cargos': estados_cargos})
        #
        # end func
        return render(request, self.template_name, {'docentes': listado})
