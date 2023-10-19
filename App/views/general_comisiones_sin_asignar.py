from django.views.generic import TemplateView
from django.shortcuts import render
from collections import defaultdict
from django.utils import timezone

from App.models.mapa_de_carreras import *

class GeneralComisionesSinAsignar(TemplateView):
    template_name = 'general_comisiones_sin_asignar.html'
    
    def get(self, request):
        
        # Versión con ORM pero que no recuparaba los días sin cargo asignado:
        
        # current_date = timezone.now().date()

        # # Recuperar todas las materias con sus respectivas carreras asociadas
        # materias_carreras = Materia_Carrera.objects.select_related('materia', 'carrera').all()

        # # Crear un diccionario para agrupar carreras por nombre de materia
        # carreras_por_materia = defaultdict(set)

        # for mc in materias_carreras:
        #     materia_nombre = mc.materia.nombre
        #     carrera_nombre = mc.carrera.nombre
        #     carreras_por_materia[materia_nombre].add(carrera_nombre)

        # # Crear una lista de diccionarios con el nombre de la materia y las carreras asociadas
        # materias_con_carreras = []

        # for materia, carreras in carreras_por_materia.items():
        #     materias_con_carreras_dict = {
        #         'nombre_materia': materia,
        #         'nombres_carreras': list(carreras)  # Convertir el conjunto en una lista
        #     }
        #     materias_con_carreras.append(materias_con_carreras_dict)

        # # Ahora, puedes usar esta lista de materias con carreras para recuperar otros datos
        # comisiones = Comision.objects.filter(
        #     comision_ch__cargo_cte_ch__isnull=True,
        #     comision_ch__carga_horaria__fecha_hasta__gte=current_date
        # ).values(
        #     'nombre',  # Nombre de la comisión
        #     'materia__nombre',  # Nombre de la materia
        #     'ubicacion__nombre'  # Nombre de la ubicación
        # )

        # # Crear un diccionario para agrupar comisiones por nombre de materia
        # comisiones_por_materia = defaultdict(list)

        # for comision in comisiones:
        #     comision_nombre = comision['nombre']
        #     materia_nombre = comision['materia__nombre']
        #     ubicacion_nombre = comision['ubicacion__nombre']
        #     comisiones_por_materia[materia_nombre].append((comision_nombre, ubicacion_nombre))

        # # Crear una lista de diccionarios con el nombre de la comisión, el nombre de la materia, el nombre de la ubicación y las carreras
        # comisiones_concatenadas = []

        # for materia, comisiones_ubicacion in comisiones_por_materia.items():
        #     comisiones_materia_dict = {
        #         'nombre_comision': comisiones_ubicacion[0][0],  # Tomar el nombre de la primera comisión
        #         'nombre_materia': materia,
        #         'nombre_ubicacion': comisiones_ubicacion[0][1],  # Tomar el nombre de la primera ubicación
        #         'nombres_carreras': next(
        #             (m['nombres_carreras'] for m in materias_con_carreras if m['nombre_materia'] == materia), []
        #         )
        #     }
        #     comisiones_concatenadas.append(comisiones_materia_dict)

        # for c in comisiones_concatenadas: print(c)        
        

        # Versión SQL, ojo seguridad:

        # ¡¡¡¡¡¡¡¡¡¡ OJO, PROBLEMAS DE SEGURIDAD !!!!!!!!!!!!!!!
        # FALTÓ PASAR ESTO A CONSULTA TIPO ORM de DJANGO, no lo logré, por eso lo dejé tal cual
        # ¡¡¡¡¡¡¡¡¡¡ OJO, PROBLEMAS DE SEGURIDAD !!!!!!!!!!!!!!!

        from django.db import connection

        query = """
            SELECT
                ac.nombre AS nombre_comision,
                am.nombre AS nombre_materia,
                au.nombre,
                STRING_AGG(DISTINCT ac2.nombre, ', ') AS nombres_carreras,
                STRING_AGG(DISTINCT ach.dia_semana, ', ') AS dias_semana
            FROM "App_comision" ac
            INNER JOIN "App_comision_ch" acc ON acc.comision_id = ac.id
            INNER JOIN "App_carga_horaria" ach ON ach.id = acc.carga_horaria_id
            INNER JOIN "App_materia" am ON am.id = ac.materia_id
            INNER JOIN "App_materia_carrera" amc ON amc.materia_id = am.id
            INNER JOIN "App_carrera" ac2 ON ac2.id = amc.carrera_id
            inner join "App_ubicacion" au on au.id = ac.ubicacion_id 
            WHERE ach.fecha_hasta >= current_date
            AND (
                ach.id NOT IN (
                    SELECT ach2.id 
                    FROM "App_comision_ch" acc2
                    INNER JOIN "App_carga_horaria" ach2 ON ach2.id = acc2.carga_horaria_id
                    INNER JOIN "App_cargo_cte_ch" accc ON accc.comision_ch_id = acc2.id
                    WHERE ach2.fecha_hasta >= current_date
                )
            ) 
            GROUP BY ac.nombre, am.nombre, au.nombre;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            comisiones = cursor.fetchall()

        for c in comisiones: print(c)

        return render(request, self.template_name, {
            # 'comisiones': comisiones_concatenadas
            'comisiones': comisiones
        })