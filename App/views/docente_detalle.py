from django.views.generic import TemplateView
from django.shortcuts import render
import requests
from requests.exceptions import ConnectTimeout
import datetime
from App.models.mapa_de_carreras import *
from App.models.guarani import *


class DocenteDetalleView(TemplateView): # Detalle para un único docente
    template_name = 'docente_detalle.html'
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request, legajo): # Se puede recuperar el param atr llamándolo como esta definido en urls.py en este caso: legajo
        legajo = str(legajo) # TODO: Revisar si la conversión afecta a las consultas a la base de datos. En el modelo, legajo es Integer     
        
        # Info persona docente ---------------------------------------------------
        docente = None # Inicializo
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
            cargos_activos = None
            return render(request, self.template_name, {'docente': docente, 'cargos':cargos_activos}) # materias, comisiones...

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
        
        ###################################################################################################################################
        # TAREA: poner la restricción y definir la modalidad correspondiente, semi y exclusivo solo pueden tener una modadlidad posible.
        # el único que puede llegar a quedar en blanco, es el semi
        ###################################################################################################################################

        # Info cargo docente --------------------------------------------------------
        cargos = None # Hay que inicializar sí o sí, sino no se van a cargar los nuevos valores del if que viene más abajo
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

                    ###################
                    #       NEW       #  
                    ###################

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
                    

                    # Caso: cargo existe en la BD, realizamos actualización de datos
                    if Cargo.objects.filter(nro_cargo=c.get('cargo')).exists(): # Update si hubo cambios (intuímos por error en mapuche), errores no nos interesa dejar como histórico
                        cargo = Cargo.objects.get(nro_cargo=c.get('cargo')) # Recupero el cargo que voy a actualizar

                        cargo.modalidad = modalidad # 
                        cargo.dedicacion = dedicacion # 
                        cargo.categoria = categoria
                        cargo.categoria = categoria
                        cargo.fecha_alta = c.get('fecha_alta')
                        cargo.fecha_baja = c.get('fecha_baja')
                        cargo.save()
                    else: 
                        cargo = Cargo.objects.create(
                            nro_cargo = c.get('cargo'),
                            docente = docente,
                            # resol -> Default,
                            # depend_desemp -> Default, TODO: asociar data Guaraní
                            # depend_design -> Ídem depend_desemp,
                            # cargas de horarias -> TODO: faltan definirlas bien
                            categoria = categoria,
                            dedicacion = dedicacion,
                            modalidad = modalidad,
                            fecha_alta = c.get('fecha_alta'),
                            fecha_baja = c.get('fecha_baja')
                        )
                    
                    aux_dict['cargo'] = cargo
                    aux_dict['categoria'] = categoria
                    aux_dict['dedicacion'] = dedicacion
                    aux_dict['modalidad'] = modalidad
                    # dependencias -> TODO: Relacionar con los datos de Guaraní
                    # cargas de horarias -> TODO: faltan definirlas bien
                    
                    #
                    fecha_baja = None # Inicializo para usar dentro del if y almacenar el valor
                    # print('fecha baja: ',aux_dict['fecha_baja'])
                    # IMPORTANTE: los valores null de la API se traducen a None implícitamente
                    if aux_dict['cargo'].fecha_baja is not None:
                        fecha_baja = datetime.datetime.strptime(aux_dict['cargo'].fecha_baja, '%Y-%m-%d').date()
                    cur_date = datetime.date.today() # Debería venir en formato yyyy-mm-dd
                    # Add a cargos_activos // para el template
                    if (fecha_baja is None) or (fecha_baja >= cur_date): # REVISAR SI EL null DE LA API ES UN null de python O SI LLEGA COMO UN STRING
                        cargos_activos.append(aux_dict)

        except ConnectTimeout: pass
        
        if (cargos is None) and (Cargo.objects.filter(docente=docente).exists()): # Lo recupero
            cargos = Cargo.objects.all(docente=docente)
            for c in cargos:
                aux_dict['cargo'] = cargo
                aux_dict['categoria'] = categoria
                aux_dict['dedicacion'] = dedicacion
                aux_dict['modalidad'] = modalidad
                # dependencias -> TODO: Relacionar con los datos de Guaraní
                # cargas de horarias -> TODO: faltan definirlas bien
                #
                fecha_baja = None
                if aux_dict['cargo'].fecha_baja is None: fecha_baja = datetime.datetime.strptime(aux_dict['cargo'].fecha_baja, '%Y-%m-%d').date()
                cur_date = datetime.date.today()
                if (fecha_baja is None) or (fecha_baja >= cur_date): cargos_activos.append(aux_dict)

        # Dependencia de designación # Por ahora no sabemos de donde sacarla
        # Dependencia desempeño      # Ídem 
        
        # Carrera         --> Vamos a tirar directamente la propuesta
        # Materia         --> elemento.nombre (sga_elementos)
        # Comisión        --> 
        # Franja horaria  --> 
        # Periodo lectivo --> fecha_inicio, fecha_finalización (sga_comisiones_bh)
        # Total horas     --> 
        # print(sga_elementos.objects.using('guarani').all())
        # # usuarios_externos = UsuarioExterno.objects.using('db_externa').all()

        # Sólo aplica el caso de "Existe" una carga_horaria asignada al docente... Sino no debería mostrar nada...
        if cargos_activos is not None:
            for dict in cargos_activos:
                c = dict.get('cargo')
                cargas_horarias = Carga_Horaria.objects.filter(cargo=c) # Puedo recibir más de uno... uso filter
                dict['carga_horaria'] = []
                if cargas_horarias: # Contiene elementos
                    for ch in cargas_horarias: 
                        # Es carga de materia o de tipo extra?
                        if ch.comision: # Es no None --> Recupero materia y plan de estudio
                            
                            # Tema n:n
                            # recupera materia --> elemento
                            # Tema n:n
                            # recupera carrera --> plan de estudios 
                        
                            print(ch.comision)
                        # dict['carga_horaria'].append(ch)
                
                    
                


        # Funciona correcto!
        # materias = Materias.objects.using('guarani').all()
        # for materia in materias:
        #     print(materia.nombre)
  
        return render(request, self.template_name, {'docente': docente, 'cargos':cargos_activos}) # materias, comisiones...

        


