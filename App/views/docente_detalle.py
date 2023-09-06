from django.views.generic import TemplateView
from django.shortcuts import render
import requests
from requests.exceptions import ConnectTimeout
from datetime import datetime, date, timedelta
from App.models.mapa_de_carreras import *
from App.models.guarani import *
from django.db.models import Q

import math
from decimal import Decimal
from django.utils import timezone

class DocenteDetalleView(TemplateView): # Detalle para un único docente
    template_name = 'docente_detalle.html'
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'
    
    alert = None
    cargos_activos = None

    def get(self, request, legajo): # Se puede recuperar el param atr llamándolo como esta definido en urls.py en este caso: legajo
        legajo = str(legajo) # TODO: Revisar si la conversión afecta a las consultas a la base de datos. En el modelo, legajo es Integer     
        
        docente = None # Inicializo
        cargos = None 
        cargos_activos = None
        cargas_cte_ch = None

        # .............................................................................. #
        # ............................ Info persona docente ............................ #
        # .............................................................................. #
        url = self.url_mapuche+'agentes/'+legajo # /agentes/{legajo}
        try:
            response = requests.get(url, auth=(self.username, self.password), timeout=5)
            if response.status_code == 200:
                data = response.json()
                # Recuperación o creación en la base de datos (en caso de no existir)
                if Docente.objects.filter(legajo=legajo).exists(): 
                    docente = Docente.objects.get(legajo=legajo)
                    docente.numero_documento = data.get('numero_documento')
                    docente.nombre_apellido  = data.get('agente')
                    # No actualizo el legajo porque no tiene sentido... Si se hubiese cambiado el legajo no lo hubiese encontrado...
                    docente.save() 
                else:
                    docente = Docente.objects.create(
                        numero_documento = data.get('numero_documento'),
                        legajo           = data.get('legajo'),
                        nombre_apellido  = data.get('agente')
                    )
        except ConnectTimeout:
            # Se trata al final junto con el status_code <> 200
            pass 
        #
        if (docente is None) and (Docente.objects.filter(legajo=legajo).exists()):
            docente = Docente.objects.get(legajo=legajo) # Lo recupero
        elif (docente is None) and (not Docente.objects.filter(legajo=legajo).exists()): 
            DocenteDetalleView.cargos_activos = None
            return render(request, self.template_name, {'docente': docente, 'cargos_activos': cargos_activos, 'cargas_cte_ch': cargas_cte_ch, 'cargos_horas': None }) # Faltaría agregar las materias, comisiones... que también serían = None

        # Correo docente --------------------------------------------------------
        if docente is not None:
            url = self.url_mapuche+'agentes/'+legajo+'/mail' # /agentes/{legajo}/mail
            try:
                response = requests.get(url, auth=(self.username, self.password), timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if len(data) > 0:
                        docente.correo_electronico = data[0].get('correo_electronico')
                        docente.save()
            except ConnectTimeout: pass # Si no se pudo recuperar el correo de la API se muestra lo que tenga cargado -> None o sumail@untdf.edu.ar
        # print(docente.correo_electronico)
        

        # Info cargo docente --------------------------------------------------------
        cargos_activos = [] # Lista de diccionarios auxiliar, facilita mostrar nombre de categoria, dedicación, otros. En lugar de mostrar solo el código  
        url = self.url_mapuche+'agentes/'+legajo+'/cargos' # /agentes/{legajo}/cargos
        try:
            response = requests.get(url, auth=(self.username, self.password), timeout=5)
            if response.status_code == 200:
                cargos = response.json()
                # Para este punto la categoria y el docente asociado al cargo ya están definidos, en caso de algún inconveninete sale antes
                for c in cargos:
                    # print(c)
                    cargo = None
                    aux_dict = {}
                    
                    # Categoria
                    categoria, _ = Categoria.objects.get_or_create(
                        codigo=c.get('categoria'), 
                        desc_categ=c.get('desc_categ')
                    )

                    # DEDICACIÓN:
                    # Simple    =>  { 'Docencia/Desarrollo profesional' }
                    # Exclusivo =>  { 'Docencia e Investigación' }
                    # Semided.  =>  { 'Docencia/Desarrollo profesional' OR 'Docencia e Investigación' }

                    # Dedicación: desde Mapuche vienen como: --> {'Simple', 'Semided.', 'Exclusiva'} <--
                    dedicacion, _ = Dedicacion.objects.get_or_create(desc_dedic=c.get('desc_dedic'))
                    
                    # Modalidad: sobre la dedicación recuperada, tomamos la decisión de qué valor puede tomar modalidad
                    if 'Simple' in dedicacion.desc_dedic:
                        modalidad, _ = Modalidad.objects.get_or_create(desc_modal='Docencia/Desarrollo profesional')
                    elif 'Exclusiva' in dedicacion.desc_dedic:
                        modalidad, _ = Modalidad.objects.get_or_create(desc_modal='Docencia e Investigación')
                    # Caso else: en principio sería por descarte "Semiexclusiva" o "Semided." (que es como lo llaman en Mapuche)
                    else:
                        # Lo puedo dejar en null hasta que se la asignen, está permitido en nuestro modelo, luego en "ASIGNAR MODALIDAD" se recuperará una de las dos desc_modal posibles y se le asignará
                        modalidad = None
                    
                    #
                    fecha_baja = None # Inicializo para usar dentro del if y almacenar el valor
                    activo = None # Ídem
                    # print('fecha baja: ',aux_dict['fecha_baja'])
                    
                    #...................................................................................#
                    # !Comment IMPORTANTE: los valores null de la API se traducen a None implícitamente
                    
                    if c.get('fecha_baja') is not None: # Obtengo el valor de la fecha_baja para poder comparar
                        fecha_baja = datetime.strptime(c.get('fecha_baja'), '%Y-%m-%d').date()
                    fecha_actual = date.today() # Obtengo la fecha actual
        
                    if (fecha_baja is None) or (fecha_baja >= fecha_actual): # Comparo los dates obtenidos y Add a cargos_activos // para el template
                        activo = 1
                        # cargos_activos.append(aux_dict) --> Lo hago en una recorrida de los cargos activos
                    else: activo = 0 # Else --> fecha_baja < fecha_actual(fecha_actual)


                    # Caso: cargo existe en la BD, realizamos actualización de datos
                    if Cargo.objects.filter(nro_cargo=c.get('cargo')).exists(): # Update si hubo cambios (intuímos por error en mapuche), errores no nos interesa dejar como histórico
                        cargo = Cargo.objects.get(nro_cargo=c.get('cargo')) # Recupero el cargo que voy a actualizar

                        cargo.modalidad = modalidad # 
                        cargo.dedicacion = dedicacion # 
                        cargo.categoria = categoria
                        cargo.categoria = categoria
                        cargo.fecha_alta = c.get('fecha_alta')
                        cargo.fecha_baja = c.get('fecha_baja')
                        cargo.activo = activo
                        cargo.save()
                    else: 
                        cargo = Cargo.objects.create(
                            nro_cargo = c.get('cargo'),
                            docente = docente,
                            # resol -> Default,
                            # depend_desemp -> Default, TODO: asociar data Guaraní
                            # depend_design -> Ídem depend_desemp,
                            categoria = categoria,
                            dedicacion = dedicacion,
                            modalidad = modalidad,
                            fecha_alta = c.get('fecha_alta'),
                            fecha_baja = c.get('fecha_baja'),
                            activo = activo
                        )         
        except ConnectTimeout: pass # Lo trato a continuación:
        
        # Si se lograron almacenar cargos para el docente, los voy a almacenar los activos para poder mostrarlos por pantalla
        if (Cargo.objects.filter(docente=docente).exists()): # Caso en el que existe al menos un cargo en la BD, lo recupero
            cargos = Cargo.objects.filter(docente=docente, activo=1)
            cargas_cte_ch = []
            cargos_horas = []
            
            for c in cargos:
                cargos_activos.append(c) # Los añadimos al diccionario que recibirá al template

                # !Comment: Debería mostar algo sólo si existen cargas horarias ya creadas para el cargo, sino eso estaría vacío --> eso tiene que ser un control en el Template
                current_date = timezone.now().date()
                # cte_ch_aux = Cargo_CTE_CH.objects.filter(
                #     cargo=c,
                #     comision_ch__carga_horaria__fecha_hasta__gte=current_date
                # )
                cte_ch_aux = Cargo_CTE_CH.objects.filter(
                    Q(cargo=c) &
                    (Q(comision_ch__carga_horaria__fecha_hasta__gte=current_date) |
                    Q(tipo_extra_ch__fecha_hasta__gte=current_date))
                )
                # print(cte_ch_aux)

                total_horas = 0.00 # será un valor decimal
            
                for cte_ch in cte_ch_aux:
                    print(cte_ch.cargo)
                    cargas_cte_ch.append(cte_ch)
                    
                    if (cte_ch.comision_ch is not None): 
                        print(cte_ch.comision_ch.carga_horaria.fecha_hasta)
                        hora_inicio = cte_ch.comision_ch.carga_horaria.hora_inicio
                        hora_fin = cte_ch.comision_ch.carga_horaria.hora_fin
                        #
                        # Calcular la diferencia de tiempo manualmente
                        diferencia_horas = hora_fin.hour - hora_inicio.hour
                        if (hora_fin.minute % 10 == 9): diferencia_minutos = (hora_fin.minute - hora_inicio.minute) + 1
                        else: diferencia_minutos = hora_fin.minute - hora_inicio.minute
                        #
                        total_horas += diferencia_horas + (diferencia_minutos / 60)
                    
                    elif (cte_ch.tipo_extra_ch is not None):
                        print(cte_ch.tipo_extra_ch.fecha_hasta)
                        cant_horas_tarea = cte_ch.tipo_extra_ch.cant_horas
                        total_horas += cant_horas_tarea
                    
                    print(total_horas)

                #
                cargos_horas.append({"cargo": c, "total_horas": total_horas})

        DocenteDetalleView.cargos_activos = cargos_activos
        return render(request, self.template_name, {'docente': docente, 'cargos_activos': cargos_activos, 'cargas_cte_ch': cargas_cte_ch, 'cargos_horas': cargos_horas }) # materias, comisiones, tareas extras

        
    def post(self, request, legajo):
        for ca in DocenteDetalleView.cargos_activos:
            # print(ca)
            archivos = request.FILES.getlist('file-'+str(ca.nro_cargo))
            # print(archivo)
            if len(archivos) == 1:
                a = archivos[0]
                # print(a)
                ca.resolucion = a
                ca.save()
            
        
        # nro_cargo = request.POST.get('cargo_number')
        # print(nro_cargo)
        
        return self.get(request, legajo)