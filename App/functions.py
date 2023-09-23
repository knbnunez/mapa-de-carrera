from App.models.mapa_de_carreras import *
from django.db.models import Q
from django.utils import timezone

# --------------------------------------------------------------------------------------------------------- #
# CALCULA CARGAS HORARIAS TOTALES, LOS AGREGA AL CARGO Y RETORNA LAS INTERRELACIONES SOBRE LAS QUE SE CALCULÓ
# --------------------------------------------------------------------------------------------------------- #
def calcular_horas(legajo):
    docente = Docente.objects.get(legajo=legajo) # recuperar objeto docente
    cargos = Cargo.objects.filter(docente=docente, activo=1) # cargos sobre los que voy a calcular (e iterar)
    current_date = timezone.now().date()
    #
    cargas_cte_ch = [] # array que retornaremos
    #   
    for c in cargos:
        #
        cargas_horarias_cargos = Cargo_CTE_CH.objects.filter(
            Q(cargo=c) &
            (Q(comision_ch__carga_horaria__fecha_hasta__gte=current_date) |
            Q(tipo_extra_ch__fecha_hasta__gte=current_date))
        )
        #
        total_horas = 0.00 # valor decimal
        #
        for chc in cargas_horarias_cargos:
            #
            cargas_cte_ch.append(chc)
            #
            # CARGA DE TIPO COMISION
            if (chc.comision_ch is not None): 
                #
                hora_inicio = chc.comision_ch.carga_horaria.hora_inicio
                hora_fin = chc.comision_ch.carga_horaria.hora_fin
                diferencia_horas = hora_fin.hour - hora_inicio.hour
                #
                if (hora_fin.minute % 10 == 9): diferencia_minutos = (hora_fin.minute - hora_inicio.minute) + 1 # caso 59', 29'
                else: diferencia_minutos = hora_fin.minute - hora_inicio.minute
                #
                total_horas += diferencia_horas + (diferencia_minutos / 60)
            #
            # CARGA DE TIPO TAREA EXTRA           
            elif (chc.tipo_extra_ch is not None):
                cant_horas_tarea = chc.tipo_extra_ch.cant_horas
                total_horas += cant_horas_tarea
        #
        # Finalizando la iteración sobre la interrelación, asigno el calculo al cargo
        c.carga_actual = total_horas
        c.save()
    #
    # Fin de todos los bucles
    return cargas_cte_ch