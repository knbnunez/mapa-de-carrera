# app/views.py
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse
from App.models import *
import requests
from django.db.models import Q
import json
from requests.exceptions import ConnectTimeout


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
        else: return render(request, self.template_name, {'docente': docente, 'cargos':cargos, 'categorias':categorias})

        # Correo docente --------------------------------------------------------
        correo_electronico = None
        if docente is not None:
            url = self.url_mapuche+'agentes/'+legajo+'/mail' # /agentes/{legajo}/mail
            try:
                response = requests.get(url, auth=(self.username, self.password), timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    docente.correo_electronico = data.get('correo_electronico')
                    docente.save()
            except ConnectTimeout:
                pass # Si hubo error se mostrará el que tenga cargado el docente, y si se recuperó el correo, pero no el docente, no se mostrará el docente...
        
        # Categorías --------------------------------------------------------
        # Nota: se actualiza el listado de categorias almacenadas en la base de datos. Sirve para recuperarlas de manera posterior en 
        # url = self.url_mapuche+'categorias' # /categorias
        # try:
        #     response = requests.get(url, auth=(self.username, self.password), timeout=5)
        #     if response.status_code == 200: 
        #         data = response.json()
        #         for d in data:
        #             categoria, _ = Categoria.objects.get_or_create( # .save() implícito
        #                 categoria=d.get('categoria'),
        #                 nombre = d.get('desc_categ')
        #             )
        # except ConnectTimeout:
        #     pass
        
        # Info cargo docente --------------------------------------------------------
        cargos = None        
        url = self.url_mapuche+'agentes/'+legajo+'/cargos' # /agentes/{legajo}/cargos
        try:
            response = requests.get(url, auth=(self.username, self.password), timeout=5)
            if response.status_code == 200:
                cargos = response.json()
                # TODO: Recorrer los Cargos, para las categorias y el docente, recuperar el que coincida con la categoria y con el legajo
                #       tener en cuenta lo comentado abajo
                
                # Para este punto la categoria y el docente asociado al cargo tiene que estar definido
                for c in cargos:
                    # print(c)
                    if Cargo.objects.filter(id_cargo=c.get('cargo')).exists(): # Update si hubo cambios (intuímos por error en mapuche), errores no nos interesa dejar como histórico
                        cargo = Cargo.objects.get(id_cargo=c.get('cargo'))
                        dedicacion, _ = Dedicacion.objects.get_or_create(nombre=c.get('desc_dedic'))
                        modalidad_dedicacion, _ = Modalidad_Dedicacion.objects.get_or_create(
                            dedicacion = dedicacion,
                            modalidad = None, # IMPORTANTE: Deberán asignarsela devuelta...
                            # restriccion_horas # TODO: Pensar en el tema restricción de horas, si debería estar predefinido en el modelo, o dónde...
                            # error default = 0
                        )

                        id_dedicacion = Dedicacion.objects.get(nombre=c.get(''))
                    
                    else: # TODO: Crear un cargo nuevo para el docente

        except ConnectTimeout:
            pass
              
                    
        #             # Creación cargo
        #             if not Cargo.objects.filter(cargo=c.get('cargo')).exists(): # Caso no existe en la BD
        #                 cargo = Cargo.objects.create(
        #                     cargo = c.get('cargo'),
        #                     # legajo = jsons[0].get('legajo'), # NO FUNCIONA ASÍ, SOLUCIÓN:
        #                     legajo = docente,
        #                     # id_resolucion = Cargar más adelante...
        #                     # dependencia_desempeno = Cargar más adelante...
        #                     # dependencia_designacion = Cargar más adelante...
        #                     categoria = categoria,
        #                     # id_dedicacion_modalidad = Se carga más adelante al Asignar la Modalidad
        #                     # id_cargas_extras = Cargar más adelante...
        #                     fecha_alta = c.get('fecha_alta'),
        #                     fecha_baja = c.get('fecha_baja')
        #                 )                        
        #             else: cargo = Cargo.objects.get(cargo=c.get('cargo'))
        #             print(cargo)

        #     # Fallo en alguna de las dos consultas agentes o mail
        #     # else:
        #         # # 1. No existe en la BD -> algún mensaje en el template sobre que no está cargado
        #         # if not Docente.objects.filter(legajo=legajo).exists(): # Caso no existe en la BD
        #         #     docente = None # Luego en el template -> if docente -> muestro; else (docente = None): "no existe"
        #         # # 2. Existe en la BD -> se muestran los datos de la BD
        #         # else:
        #         #     docente = Docente.objects.get(legajo=legajo)
        # except ConnectTimeout:
        #     # if not Docente.objects.filter(legajo=legajo).exists(): docente = None 
        #     # else: docente = Docente.objects.get(legajo=legajo)
        #     pass
        # # Caso status_code <> 200 para cualquiera de las dos consultas (agentes, mail) y caso excepción ConnectTimeout, junto todo acá
        # #
        # # AGREGAR TEMA CARGO Y CATEGORIA
        # if exito != 1:   
        #     # 1. No existe en la BD -> algún mensaje en el template sobre que el docente no está cargado     
        #     if not Docente.objects.filter(legajo=legajo).exists(): # Caso no existe en la BD
        #         docente = None # Luego en el template -> if docente -> muestro; else (docente = None): "no existe"
        #     # 2. Existe en la BD -> se muestran los datos de la BD
        #     else:
        #         docente = Docente.objects.get(legajo=legajo)



        return render(request, self.template_name, {'docente': docente, 'cargos':cargos, 'categorias':categorias}) # Tratar de devolver las categorias asociadas a los cargos, no todo el listado.

        


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
