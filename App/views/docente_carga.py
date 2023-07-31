# views.py

from django.shortcuts import render
from django.views import View

from App.cargaForm import AsignarDocenteForm
from App.models.mapa_de_carreras import Carrera, Comision, Docente, Materia, Materia_Carrera

class DocenteCargaHorariaView(View):
    template_name = 'docente_carga_horaria.html'
    form_class = AsignarDocenteForm    
    username = 'mapumapa' # Para producción hay que crifrar las credenciales
    password = 'Mowozelu28'
    url_mapuche = 'http://10.7.180.231/mapuche/rest/'

    def get(self, request):
        form = self.get_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AsignarDocenteForm(request.POST)
        if form.is_valid():
            instituto = form.cleaned_data['instituto']
            carrera = form.cleaned_data['carrera']
            materia = form.cleaned_data['materia']
            comision = form.cleaned_data['comision']
            docente = form.cleaned_data['docente']

            # Realizar las acciones necesarias con los datos seleccionados
            # Por ejemplo, guardar la información en la base de datos

            return render(request, self.template_name, {'form': form, 'success': True})

        return render(request, self.template_name, {'form': form})

    def get_form(self):
        form = AsignarDocenteForm()
        form.fields['carrera'].queryset = Carrera.objects.none()
        form.fields['materia'].queryset = Materia.objects.none()
        form.fields['comision'].queryset = Comision.objects.none()
        form.fields['docente'].queryset = Docente.objects.none()

        if 'instituto' in self.request.GET:
            instituto_id = self.request.GET.get('instituto')
            form.fields['carrera'].queryset = Carrera.objects.filter(carrera_instituto__instituto_id=instituto_id)

        if 'carrera' in self.request.GET:
            carrera_id = self.request.GET.get('carrera')
            form.fields['materia'].queryset = Materia.objects.filter(materia_carrera__carrera_id=carrera_id)

        if 'materia' in self.request.GET:
            materia_id = self.request.GET.get('materia')
            form.fields['comision'].queryset = Comision.objects.filter(materia_id=materia_id)

        if 'comision' in self.request.GET:
            comision_id = self.request.GET.get('comision')
            form.fields['docente'].queryset = Docente.objects.filter(comision_id=comision_id)

        return form