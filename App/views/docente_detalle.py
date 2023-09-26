import requests
import math
from django.views.generic import TemplateView
from requests.exceptions import ConnectTimeout
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, date, timedelta
from decimal import Decimal

from App.models.mapa_de_carreras import *
from App.models.guarani import *


class DocenteDetalleView(TemplateView): # Detalle para un único docente
    template_name = 'docente_detalle.html'
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'
    
    alert = None
    cargos_activos = None

    def get(self, request, legajo): # Se puede recuperar el param de la url llamándolo como esta definido en urls.py en este caso: legajo
        legajo = str(legajo) 
        
        docente = None # Inicializo
        cargos = None 
        cargos_activos = None
        cargas_cte_ch = None
        cargos_horas = None

        ########################
        # Info persona docente #
        ########################
        url = self.url_mapuche+'agentes/'+legajo # /agentes/{legajo}
        try:
            response = requests.get(url, auth=(self.username, self.password), timeout=5)
            if ((response.status_code == 200) and (response.json() != [])):
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
        except ConnectTimeout: pass # Se trata al final junto con el status_code <> 200
        
        if (docente is None) and (Docente.objects.filter(legajo=legajo).exists()):
            docente = Docente.objects.get(legajo=legajo) # Lo recupero
        elif (docente is None) and (not Docente.objects.filter(legajo=legajo).exists()): 
            DocenteDetalleView.cargos_activos = None
            return render(request, self.template_name, { 'alert':DocenteDetalleView.alert, 'docente': docente, 'cargos_activos': cargos_activos, 'cargas_cte_ch': cargas_cte_ch, 'cargos_horas': cargos_horas }) 

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
        

        ######################
        # Info cargo docente #
        ######################
        cargos_activos = []
        url = self.url_mapuche+'agentes/'+legajo+'/cargos?activos=1' # /agentes/{legajo}/cargos
        try:
            response = requests.get(url, auth=(self.username, self.password), timeout=5)
            # print(response)
            # print(response.json())
            # print((response.json()) != [])
            if ((response.status_code == 200) and (response.json() != [])):
                cargos = response.json()
                # Para este punto la categoria y el docente asociado al cargo ya están definidos, en caso de algún inconveninete sale antes
                for c in cargos:
                    # print(c)
                    cargo = None
                                        
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
                    

                    #############################
                    # CÁLCULO DE CARGOS ACTIVOS #
                    #############################

                    try:fecha_alta = datetime.strptime(c.get('fecha_alta'), '%Y-%m-%d')
                    except: fecha_alta = None 
                    #
                    try: fecha_baja = datetime.strptime(c.get('fecha_baja'), '%Y-%m-%d')
                    except: fecha_baja = None 

                    # Caso: cargo existe en la BD, realizamos actualización de datos
                    if Cargo.objects.filter(nro_cargo=c.get('cargo')).exists(): # Update si hubo cambios (intuímos por error en mapuche), errores no nos interesa dejar como histórico
                        cargo = Cargo.objects.get(nro_cargo=c.get('cargo')) # Recupero el cargo que voy a actualizar

                        cargo.modalidad = modalidad # 
                        cargo.dedicacion = dedicacion # 
                        cargo.categoria = categoria
                        cargo.categoria = categoria
                        cargo.fecha_alta = fecha_alta
                        cargo.fecha_baja = fecha_baja
                        cargo.activo = 1
                        cargo.save()
                    else: 
                        cargo = Cargo.objects.create(
                            nro_cargo = c.get('cargo'),
                            docente = docente,
                            categoria = categoria,
                            dedicacion = dedicacion,
                            modalidad = modalidad,
                            fecha_alta = fecha_alta,
                            fecha_baja = fecha_baja,
                            activo = 1
                        )    
                         
                    # print(cargo)
                    if('nodo' not in c['escalafon'].lower().replace(" ", "")): cargos_activos.append(cargo) # Los añadimos al diccionario que recibirá al template    
        except ConnectTimeout: pass # Lo trato a continuación:
        
        # Si se lograron almacenar cargos para el docente, los voy a almacenar los activos para poder mostrarlos por pantalla
        if (Cargo.objects.filter(docente=docente, activo=1).exists()): # Caso en el que existe al menos un cargo en la BD, lo recupero
            cargos = Cargo.objects.filter(docente=docente, activo=1)
            cargas_cte_ch = []
            cargos_horas = []

            for c in cargos:
                current_date = timezone.now().date()

                cte_ch_aux = Cargo_CTE_CH.objects.filter(
                    Q(cargo=c) &
                    (Q(comision_ch__carga_horaria__fecha_hasta__gte=current_date) |
                    Q(tipo_extra_ch__fecha_hasta__gte=current_date))
                )
                # print(cte_ch_aux)

                total_horas = 0.00 # será un valor decimal
            
                for cte_ch in cte_ch_aux:
                    # print(cte_ch.cargo)
                    cargas_cte_ch.append(cte_ch)
                    
                    if (cte_ch.comision_ch is not None): 
                        # print(cte_ch.comision_ch.carga_horaria.fecha_hasta)
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
                        # print(cte_ch.tipo_extra_ch.fecha_hasta)
                        cant_horas_tarea = cte_ch.tipo_extra_ch.cant_horas
                        total_horas += cant_horas_tarea

                    # print(total_horas)
                #
                cargos_horas.append({"cargo": c, "total_horas": total_horas})

        DocenteDetalleView.cargos_activos = cargos_activos

        return render(request, self.template_name, { 'alert':DocenteDetalleView.alert, 'docente': docente, 'cargos_activos': cargos_activos, 'cargas_cte_ch': cargas_cte_ch, 'cargos_horas': cargos_horas })


    def post(self, request, legajo):
        print(f'Qué valor tiene el alert? {DocenteDetalleView.alert}')
        DocenteDetalleView.alert = None
        # Carga archivos:
        # - Los archivos PDF quedan guardados en /media, en la BD queda almacenada la ruta que enlaza al archivo "/media/nombre_archivo.pdf" 
        # - Se admite la carga de multiples archivos
        if DocenteDetalleView.cargos_activos is not None:
            for ca in DocenteDetalleView.cargos_activos:
                # print(f'Pero entra acá?')
                # print(ca)
                archivos = request.FILES.getlist('file-'+str(ca.nro_cargo))
                # print(archivo)
                if len(archivos) == 1:
                    a = archivos[0]
                    if a.content_type == 'application/pdf':
                        ca.resolucion = a
                        ca.save()
                    else:
                        # No es un archivo PDF
                        DocenteDetalleView.alert = "El archivo no es un PDF válido."
                        print(f'ERROR: {DocenteDetalleView.alert}')
                        break # Debería salir del bucle y no procesar ningún archivo más
                
        print(f'Valor de salida del alert {DocenteDetalleView.alert}')
        return self.get(request, legajo)