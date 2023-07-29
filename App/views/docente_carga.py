# views.py

from django.shortcuts import render
from django.views import View

from App.cargaForm import ComisionDocenteForm

class DocenteCargaHorariaView(View):
    template_name = 'docente_carga_horaria.html'
    form_class = ComisionDocenteForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            comision_materia = form.cleaned_data['comision_materia']
            docente_legajo_nombre = form.cleaned_data['docente_legajo_nombre']

            # Realizar las acciones necesarias con la comisión-materia y el docente seleccionado
            # Por ejemplo, guardar la información en la base de datos

            return render(request, self.template_name, {'form': form, 'success': True})

        return render(request, self.template_name, {'form': form})
