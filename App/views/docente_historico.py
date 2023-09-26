from django.views.generic import TemplateView
from django.shortcuts import render
import requests
from requests.exceptions import ConnectTimeout
from datetime import datetime, date
from App.models.mapa_de_carreras import *
from App.models.guarani import *


class DocenteHistoricoView(TemplateView): # Detalle para un único docente
    template_name = 'docente_historico.html'
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'
    
    alert = None
    cargos_historicos = None

    def get(self, request, legajo): # Se puede recuperar el param atr llamándolo como esta definido en urls.py en este caso: legajo
        legajo = str(legajo)
        
        docente = None # Inicializo
        cargos = None 
        cargos_historicos = None

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
            
        #
        if (docente is None) and (Docente.objects.filter(legajo=legajo).exists()):
            docente = Docente.objects.get(legajo=legajo) # Lo recupero
        elif (docente is None) and (not Docente.objects.filter(legajo=legajo).exists()): 
            DocenteHistoricoView.cargos_historicos = None
            return render(request, self.template_name, {'docente': docente, 'cargos_historicos': cargos_historicos })

        
        ######################
        # Info cargo docente #
        ######################
        cargos_historicos = [] # Lista de diccionarios auxiliar, facilita mostrar nombre de categoria, dedicación, otros. En lugar de mostrar solo el código  
        url = self.url_mapuche+'agentes/'+legajo+'/cargos' # /agentes/{legajo}/cargos
        try:
            response = requests.get(url, auth=(self.username, self.password), timeout=5)
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

                    ###############
                    # DEDICACIÓN: #
                    ###############
                    #
                    # Simple    =>  { 'Docencia/Desarrollo profesional' }
                    # Exclusivo =>  { 'Docencia e Investigación' }
                    # Semided.  =>  { 'Docencia/Desarrollo profesional' OR 'Docencia e Investigación' }

                    dedicacion, _ = Dedicacion.objects.get_or_create(desc_dedic=c.get('desc_dedic'))
                    
                    # Modalidad: desde la dedicación recuperada, tomamos la decisión sobre qué valor puede tomar su modalidad
                    if 'Simple' in dedicacion.desc_dedic:
                        modalidad, _ = Modalidad.objects.get_or_create(desc_modal='Docencia/Desarrollo profesional')
                    elif 'Exclusiva' in dedicacion.desc_dedic:
                        modalidad, _ = Modalidad.objects.get_or_create(desc_modal='Docencia e Investigación')
                    # Caso else: en principio sería por descarte "Semiexclusiva" o "Semided." (que es como lo llaman en Mapuche)
                    else:
                        # Lo puedo dejar en null hasta que se la asignen, está permitido en nuestro modelo, luego en "ASIGNAR MODALIDAD" se recuperará una de las dos desc_modal posibles y se le asignará
                        modalidad = None
                    
                    #########################################
                    # Tratamiento de fechas, cargos activos #
                    #########################################
                    try:fecha_alta = datetime.strptime(c.get('fecha_alta'), '%Y-%m-%d')
                    except: fecha_alta = None 
                    #
                    try: fecha_baja = datetime.strptime(c.get('fecha_baja'), '%Y-%m-%d')
                    except: fecha_baja = None                     
                    
                    fecha_actual = datetime.combine(date.today(), datetime.min.time())
                    #
                    if (fecha_baja is None) or (fecha_baja >= fecha_actual): activo = 1
                    else: activo = 0

                    ##############################################
                    # CONSULTA EN BASE, CREAR O ACTUALIZAR DATOS #
                    ##############################################
        
                    ####################
                    # ACTUALIZAR DATOS #
                    ####################
                    if Cargo.objects.filter(nro_cargo=c.get('cargo')).exists(): # Update si hubo cambios (intuímos por error en mapuche), errores no nos interesa dejar como histórico
                        cargo = Cargo.objects.get(nro_cargo=c.get('cargo')) # Recupero el cargo que voy a actualizar
                        #
                        cargo.modalidad = modalidad # 
                        cargo.dedicacion = dedicacion # 
                        cargo.categoria = categoria
                        cargo.categoria = categoria
                        cargo.fecha_alta = fecha_alta
                        cargo.fecha_baja = fecha_baja
                        cargo.activo = activo
                        cargo.save()
                    ##################
                    # CREAR REGISTRO #
                    ##################
                    else: 
                        cargo = Cargo.objects.create(
                            nro_cargo = c.get('cargo'),
                            docente = docente,
                            categoria = categoria,
                            dedicacion = dedicacion,
                            modalidad = modalidad,
                            fecha_alta = fecha_alta,
                            fecha_baja = fecha_baja,
                            activo = activo
                        )     

                    cargos_historicos.append(cargo)
        #
        except ConnectTimeout: pass # Lo trato a continuación:
    
        DocenteHistoricoView.cargos_historicos = cargos_historicos

        # for c in cargos_historicos: print(f"{c}, activo? {c.activo}")

        return render(request, self.template_name, {'docente': docente, 'cargos_historicos': cargos_historicos }) 
    
        
    def post(self, request, legajo):
        for ca in DocenteHistoricoView.cargos_historicos:
            # print(ca)
            archivos = request.FILES.getlist('file-'+str(ca.nro_cargo))
            # print(archivo)
            if len(archivos) == 1:
                a = archivos[0]
                # print(a)
                ca.resolucion = a
                ca.save()
        
        return self.get(request, legajo)