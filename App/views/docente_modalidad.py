from django.views.generic import TemplateView
from django.shortcuts import render
from App.models.mapa_de_carreras import *
import requests
import json
from requests.exceptions import ConnectTimeout


class DocenteModalidadView(TemplateView):
    template_name = 'docente_modalidad.html'
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