from django.views.generic import TemplateView
from django.shortcuts import render
from App.models.mapa_de_carreras import *

# TODO: Cambiar a "Cargos_Activos"


# NOTA: CONSIDERAMOS QUE: SI YA PASARON POR LA PANTALLA DE DETALLE-DOCENTE PARA LLEGAR HASTA ACÁ, SIGNIFICA QUE YA SE ACTUALIZARON LOS DATOS QUE ESTABAN EN LA BASE, ASÍ QUE LOS PODEMOS CONSUMIR DIRECTAMENTE
class DocenteModalidadView(TemplateView):
    template_name = 'docente_modalidad.html'
    alert = None

    def get(self, request, legajo):
        legajo = str(legajo) 
        docente = Docente.objects.get(legajo=legajo)
        # -->   # cargos = Cargo.objects.filter(docente=docente, activo=1) # = cargos_activos
        cargos = Cargo.objects.filter(docente=docente) 
        modalidades = Modalidad.objects.all

        return render(request, self.template_name, {'docente': docente, 'cargos': cargos, 'modalidades': modalidades, 'alert': self.alert})


    # ----------- Aux ----------- #
    # Si se encuentra el valor del select_cargo dentro de los cargos activos y se comprueba que el valor de select_modalidad
    # tenga sentido con la restricción de negocio, entonces es_valido = True
    def verif_inputs(self, legajo, select_cargo, select_modalidad):
        es_valido = False
                
        legajo = str(legajo) 
        docente = Docente.objects.get(legajo=legajo)
        # -->   # cargos = Cargo.objects.filter(docente=docente, activo=1) # = cargos_activos
        cargos = Cargo.objects.filter(docente=docente)
        
        for cargo in cargos: 
            if (select_cargo == cargo.nro_cargo): # debería ocurrir una sola vez (única), cuando se encuentre el cargo relacionado al nro
                if (((cargo.dedicacion.desc_dedic == "Simple") and (select_modalidad == "Docencia/Desarrollo profesional"))
                    or ((cargo.dedicacion.desc_dedic == "Exclusiva") and (select_modalidad == "Docencia e Investigación"))
                    or ((cargo.dedicacion.desc_dedic == "Semided.") and ((select_modalidad == "Docencia/Desarrollo profesional") or (select_modalidad == "Docencia e Investigación")))
                    ): es_valido = True
                else: es_valido = False
        return es_valido
    # ----------- xxx ----------- #


    def post(self, request, legajo):
        select_cargo = request.POST.get('select-cargo')
        print(select_cargo)
        
        select_modalidad = request.POST.get('select-modalidad')
        print(select_modalidad)
        
        if (((select_cargo is not None) and (select_modalidad is not None)) and (self.verif_inputs(legajo, int(select_cargo), select_modalidad))):
            cargo = Cargo.objects.get(nro_cargo=select_cargo)
            modalidad = Modalidad.objects.get(desc_modal=select_modalidad)
            cargo.modalidad = modalidad
            cargo.save()
            self.alert = None
        else:
            self.alert = "El Cargo y/o la Modalidad estaban vacíos al momento de Guardar cambios"
        return self.get(request, legajo=legajo) # invoco al método get declarado arriba