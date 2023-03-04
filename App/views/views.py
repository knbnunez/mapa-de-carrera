# app/views.py
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse
from App.models import *
import requests
from django.db.models import Q
import json
from requests.exceptions import ConnectTimeout
import datetime


class IndexView(TemplateView):
    template_name = 'index.html' 


class DocenteDetalleView(TemplateView): # Detalle para un único docente
    template_name = 'docente-detalle.html'
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request, legajo): # Se puede recuperar el param atr llamándolo como esta definido en urls.py en este caso: legajo
        legajo = str(legajo) # TODO: Revisar si la conversión afecta a las consultas a la base de datos. En el modelo, legajo es Integer     
        
        # Info persona docente ---------------------------------------------------
        docente = None
        url = self.url_mapuche+'agentes/'+legajo # /agentes/{legajo}
        try:
            response = requests.get(url, auth=(self.username, self.password), timeout=5)
            if response.status_code == 200:
                data = response.json()
                if Docente.objects.filter(legajo=legajo).exists(): # Existe en la DB UPDATE
                    docente = Docente.objects.get(legajo=legajo)
                    docente.numero_documento = data.get('numero_documento')
                    docente.nombre_apellido  = data.get('agente')
                    docente.save() # No actualizo el legajo porque no tiene sentido... Si se hubiese cambiado el legajo no lo hubiese encontrado...
                else: # No existe en la DB CREATE
                    docente = Docente.objects.create(
                        numero_documento = data.get('numero_documento'),
                        legajo           = data.get('legajo'),
                        nombre_apellido  = data.get('agente')
                    )
        except ConnectTimeout:
            pass # Se trata al final junto con el status_code <> 200
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
                    dedicacion, _ = Dedicacion.objects.get_or_create(desc_dedic=c.get('desc_dedic'))
                    # print('dedicacion: ',dedicacion)
                    # print(f"categoria: {c.get('categoria')}. descripcion: {c.get('desc_categ')}")
                    categoria, _ = Categoria.objects.get_or_create(
                        codigo=c.get('categoria'), 
                        desc_categ=c.get('desc_categ')
                    )
                    if Cargo.objects.filter(nro_cargo=c.get('cargo')).exists(): # Update si hubo cambios (intuímos por error en mapuche), errores no nos interesa dejar como histórico
                        cargo = Cargo.objects.get(nro_cargo=c.get('cargo')) # Recupero el cargo que voy a actualizar
                        # Modalidad-Dedicación
                        modalidad_dedicacion = Modalidad_Dedicacion.objects.get(id=cargo.modalidad_dedicacion.id)
                        modalidad_dedicacion.dedicacion = dedicacion # Update dedicación por las dudas de que haya cambiado.
                        modalidad_dedicacion.save()
                        # Actualizo
                        cargo.modalidad_dedicacion = modalidad_dedicacion
                        cargo.categoria = categoria
                        cargo.fecha_alta = c.get('fecha_alta')
                        cargo.fecha_baja = c.get('fecha_baja')
                        cargo.save()
                    else: 
                        modalidad_dedicacion = Modalidad_Dedicacion.objects.create(
                            # modalidad -> la definimos luego
                            dedicacion = dedicacion
                            # restriccion de horas se definen implícitamente cuando se le asigne modalidad
                            # error -> no
                        )
                        cargo = Cargo.objects.create(
                            nro_cargo = c.get('cargo'),
                            docente = docente,
                            # resol -> Default,
                            # depend_desemp -> Default, TODO: asociar data Guaraní
                            # depend_design -> Ídem depend_desemp,
                            modalidad_dedicacion = modalidad_dedicacion,
                            # cargas de horarias -> TODO: faltan definirlas bien
                            categoria = categoria,
                            fecha_alta = c.get('fecha_alta'),
                            fecha_baja = c.get('fecha_baja')
                        )
                    
                    aux_dict['cargo'] = cargo
                    # dependencias -> TODO: Relacionar con los datos de Guaraní
                    aux_dict['dedicacion'] = dedicacion
                    # cargas de horarias -> TODO: faltan definirlas bien
                    aux_dict['categoria'] = categoria
                    
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
                # dependencias -> TODO: Relacionar con los datos de Guaraní
                aux_dict['dedicacion'] = dedicacion
                # cargas de horarias -> TODO: faltan definirlas bien
                aux_dict['categoria'] = categoria
                #
                fecha_baja = None
                if aux_dict['cargo'].fecha_baja is None: fecha_baja = datetime.datetime.strptime(aux_dict['cargo'].fecha_baja, '%Y-%m-%d').date()
                cur_date = datetime.date.today()
                if (fecha_baja is None) or (fecha_baja >= cur_date): cargos_activos.append(aux_dict)

        # TODO: Falta agregar la parte de los datos relacionados al cargo desde Guaraní:
        # Dependencia de designación
        # Dependencia desempeño
        # Periodo lectivo 
        # Carrera 
        # Materia 
        # Comisión 
        # Franja horaria 
        # Total horas 
  
        return render(request, self.template_name, {'docente': docente, 'cargos':cargos_activos}) # materias, comisiones...

        
class DocenteBusquedaView(TemplateView):
    template_name = 'buscadocente.html'
    username='mapumapa'
    password='Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request):
        url = reverse('buscadocente')
        url_buscadocente = self.url_mapuche+'agentes' # /agentes/{legajo}
        response = requests.get(url_buscadocente, auth=(self.username, self.password))
        # if response.status_code == 200:
        docentes = response.json()
        # print(docentes)
        return render(request, self.template_name, {'docentes': docentes})
        # else :
            # return render(request, self.template_name, {"docentes":})


class DocenteModalidadView(TemplateView):
    template_name = 'docente-modalidad.html'
    username = 'mapumapa'
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request, legajo):
        legajo = str(legajo) 
        url = self.url_mapuche+'agentes/'+legajo+'/cargos' # /agentes/{legajo}/cargos
        # TO DO: Misma lógica que en DocenteDetalle, si hay error en la consulta, etc...
        try:
            response = requests.get(url, auth=(self.username, self.password), timeout=5)
            cargos = response.json()
            # Puede ser útil el escalafon, que nos trae si es DOCE (docente), NODO, AUTO. En teoría el único que nos interesa es DOCE, por lo que capaz nos puede servir para hacer algún control...
            cargos = [{'cargo':_.get('cargo'), 'desc_dedic':_.get('desc_dedic'), 'escalafon':_.get('escalafon')} for _ in response.json()]
            # TO DO: Complejidad, traer la modalidad si hubiera una ya cargada. Cómo llegamos hasta la modalidad cargada para el cargo del docente?

            # FILTER Cargo con id_cargo
            for cargo in cargos:
                if not Cargo.objects.filter(cargo=cargo.get('cargo')).exists(): # Si no existe lo creamos
                    Cargo.objects.create(
                        cargo = cargo.get('cargo'),

                    )
            
            #  docente = Docente.objects.get(id=id)
            # cargo = Cargo.objects.filter(id_docente=docente).first()
            # ded = cargo.id_dedicacion
            # mod_ded = Modalidad_Dedicacion.objects.get(id_dedicacion=ded)
            # mod = mod_ded.id_modalidad
            # nombre_modalidad = mod.nombre

        except ConnectTimeout:
            pass
        return render(request, self.template_name, {'cargos': json.dumps(cargos)})

    # TO DO: almacenar la modalidad y la dedicación que viene en la consulta para la tabla intermedia que genera la restricción de horas + el archivo adjunto

    def post(self, request, legajo):
        
        return self.get(request, legajo) # invoco al método get declarado arriba
