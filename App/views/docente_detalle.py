import requests
from django.views.generic import TemplateView
from requests.exceptions import ConnectTimeout
from django.shortcuts import render
from datetime import datetime

from App.models.mapa_de_carreras import *
from App.models.guarani import *
from App.functions import calcular_horas


class DocenteDetalleView(TemplateView): # Detalle para un único docente
    template_name = 'docente_detalle.html'
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'
    
    alert = None
    cargos_activos = []
    info = []
    cargas_cte_ch = []

    def get(self, request, legajo): # Se puede recuperar el param de la url llamándolo como esta definido en urls.py en este caso: legajo
        legajo = str(legajo) 
        
        docente = None # Inicializo
        cargos = None 
        cargos_activos = None
        info = None

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
            return render(request, self.template_name, { 'alert':DocenteDetalleView.alert, 'docente': docente, 'cargos_activos': DocenteDetalleView.cargos_activos, 'info': DocenteDetalleView.info, 'cargas_cte_ch': DocenteDetalleView.cargas_cte_ch }) 

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
        info = []
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
                    # MARCADO DE CARGOS ACTIVOS #
                    #############################

                    try:fecha_alta = datetime.strptime(c.get('fecha_alta'), '%Y-%m-%d')
                    except: fecha_alta = None 
                    #
                    try: fecha_baja = datetime.strptime(c.get('fecha_baja'), '%Y-%m-%d')
                    except: fecha_baja = None 

                    # Caso: cargo existe en la BD, realizamos actualización de datos
                    if Cargo.objects.filter(nro_cargo=c.get('cargo')).exists(): # Update si hubo cambios (intuímos por error en mapuche), errores no nos interesa dejar como histórico
                        cargo = Cargo.objects.get(nro_cargo=c.get('cargo')) # Recupero el cargo que voy a actualizar

                        # comparo la dedicación actual con la anterior, si es nueva, la modalidad también va a cambiar
                        if cargo.dedicacion != dedicacion: 
                            cargo.dedicacion = dedicacion # 
                            cargo.modalidad = modalidad #
                        # sino: deben quedar igual para poder mantener la restricción
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
                    if('nodo' not in c['escalafon'].lower().replace(" ", "")): 
                        cargos_activos.append(cargo) # Los añadimos al diccionario que recibirá al template   
                        if cargo.modalidad is not None:
                            #
                            if cargo.dedicacion.desc_dedic == 'Semided.' and cargo.modalidad.desc_modal == 'Docencia/Desarrollo profesional':
                                info.append("Déficit: 6,0hs / Sobrecarga 10,0hs")
                            #
                            elif cargo.dedicacion.desc_dedic == 'Exclusiva' and cargo.modalidad.desc_modal == 'Docencia e Investigación':
                                info.append("Déficit: 4,0hs / Sobrecarga 8,0hs")
                            #
                            else: 
                                info.append("Déficit: 4,0hs / Sobrecarga 6,0hs")
        except ConnectTimeout: pass # Lo trato a continuación:
        #
        DocenteDetalleView.cargos_activos = cargos_activos
        DocenteDetalleView.info = info
        print(info)
        
        ###################################
        # RECUPERACIÓN DE CARGAS HORARIAS #
        ###################################
        if (Cargo.objects.filter(docente=docente, activo=1).exists()): DocenteDetalleView.cargas_cte_ch = calcular_horas(legajo)

        return render(request, self.template_name, { 'alert':DocenteDetalleView.alert, 'docente': docente, 'cargos_activos': DocenteDetalleView.cargos_activos, 'info': DocenteDetalleView.info, 'cargas_cte_ch': DocenteDetalleView.cargas_cte_ch })


    def post(self, request, legajo):
        #
        DocenteDetalleView.alert = None

        # Carga archivos:
        # - Los archivos PDF quedan guardados en /media, en la BD queda almacenada la ruta que enlaza al archivo "/media/nombre_archivo.pdf" 
        # - Se admite la carga de multiples archivos

        # Verificar si se envió el formulario de carga de archivos
        if 'submit_archivos' in request.POST:
            for c in DocenteDetalleView.cargos_activos:
                campo_archivo = 'file-' + str(c.nro_cargo)
                if campo_archivo in request.FILES:
                    archivo = request.FILES[campo_archivo]
                    if archivo.content_type == 'application/pdf':
                        c.resolucion = archivo
                        c.save()
                    else:
                        DocenteDetalleView.alert = "El archivo no es un PDF válido."
                        print(f'ERROR: {DocenteDetalleView.alert}')
                        break
        
        if 'submit_checkboxes' in request.POST:
            for c_c in DocenteDetalleView.cargas_cte_ch:
                checkbox = f'check-{c_c.pk}'
                if checkbox in request.POST:
                    try:
                        obj = Cargo_CTE_CH.objects.get(pk=c_c.pk)
                        obj.delete()
                    except: pass
                
        return self.get(request, legajo)