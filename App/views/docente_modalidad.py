from django.views.generic import TemplateView
from django.shortcuts import render
from App.models.mapa_de_carreras import *
# import json
# from django.core import serializers


# NOTA: CONSIDERAMOS QUE: SI YA PASARON POR LA PANTALLA DE DETALLE-DOCENTE PARA LLEGAR HASTA ACÁ, SIGNIFICA QUE YA SE ACTUALIZARON LOS DATOS QUE ESTABAN EN LA BASE, ASÍ QUE LOS PODEMOS CONSUMIR DIRECTAMENTE
class DocenteModalidadView(TemplateView):
    template_name = 'docente_modalidad.html'
    username = 'mapumapa'
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request, legajo):
        legajo = str(legajo) 
        docente = Docente.objects.get(legajo=legajo)
        # cargos = Cargo.objects.filter(docente=docente, activo=1) # = cargos_activos
        cargos = Cargo.objects.filter(docente=docente) 
        modalidades = Modalidad.objects.all

        return render(request, self.template_name, {'docente': docente, "cargos": cargos, 'modalidades': modalidades})

    # TO DO: almacenar la modalidad y la dedicación que viene en la consulta para la tabla intermedia que genera la restricción de horas + el archivo adjunto

    def post(self, request, legajo):
        select_cargo = request.POST.get('select-cargo')
        print(select_cargo)
        select_modalidad = request.POST.get('select-modalidad')
        print(select_modalidad)
        # file_input = request.POST.get('file-input')
        # print(file_input)
        if ((select_cargo is not None) and (select_modalidad is not None)):
            cargo = Cargo.objects.get(nro_cargo=select_cargo)
            modalidad = Modalidad.objects.get(desc_modal=select_modalidad)
            cargo.modalidad = modalidad
            cargo.save()
        return self.get(request, legajo) # invoco al método get declarado arriba