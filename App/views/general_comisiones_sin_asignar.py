from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import Q, Max
from django.utils import timezone

from App.models.mapa_de_carreras import *

class ComisionAux:
    def __init__(self, comision, carreras):
        self.comision = comision #objeto Comision
        self.carreras = carreras #array
    def __str__(self):
        strcar = ""
        for c in self.carreras: strcar += c.nombre
        return self.comision.nombre + strcar

class GeneralComisionesSinAsignar(TemplateView):
    template_name = 'general_comisiones_sin_asignar.html'
    
    def get(self, request):
        current_date = timezone.now().date()
        #
        comisiones = []
        
        # Consulta para recuperar las comisiones que cumplen con los criterios
        
        # Anota la fecha máxima de Carga_Horaria relacionada para cada Comision
        comisiones_con_fecha_max = Comision.objects.annotate(
            fecha_max_carga_horaria=Max('comision_ch__carga_horaria__fecha_hasta')
        )

        # Filtra las comisiones que no tienen cargo asignado y cumplen con la fecha_hasta
        comisiones_sin_cargo = comisiones_con_fecha_max.filter(
            comision_ch__cargo_cte_ch__isnull=True, # CAMBIAR POR TRUE
            fecha_max_carga_horaria__gte=current_date
        )
        # print(comisiones_sin_cargo)
        

        for com in comisiones_sin_cargo:
            materia = com.materia
            materias = Materia_Carrera.objects.filter(materia=materia)
            carreras = []
            for m in materias: carreras.append(m.carrera)
            comisiones.append(ComisionAux(com, carreras))
            # print(ComisionAux(com, carreras))


        

        # print(carreras_relacionadas)

        return render(request, self.template_name, {'comisiones': comisiones})
