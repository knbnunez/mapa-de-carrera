from django.urls import path
#from .views.carga_datos import *
from .views.index import *
from .views.docente_busqueda import *
from .views.docente_detalle import *
from .views.docente_modalidad import *
from .views.docente_tareas import *
from .views.docente_comision import *
from .views.docente_carga import *

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('', DocenteBusquedaView.as_view(), name='docente'),
    path('docentes/', DocenteBusquedaView.as_view(), name='docente'),
    path('docentes/carga-horaria', DocenteCargaHorariaView.as_view(), name='docente-carga'),
    path('docentes/<int:legajo>/detalles', DocenteDetalleView.as_view(), name='docente-detalle'),
    path('docentes/<int:legajo>/asignar-modalidad', DocenteModalidadView.as_view(), name='docente-asignar-modalidad'),
    path('docentes/<int:legajo>/asignar-tareas', DocenteTareasView.as_view(), name='docente-asignar-tareas'),
    path('docentes/<int:legajo>/asignar-comision', DocenteComisionView.as_view(), name='docente-asignar-comision'),
    ]