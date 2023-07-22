from django.urls import path
#from .views.carga_datos import *
from .views.index import *
from .views.docente_busqueda import *
from .views.docente_detalle import *
from .views.docente_modalidad import *
from .views.docente_tareas import *


urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    path('', DocenteBusquedaView.as_view(), name='docente'),
    path('docentes/', DocenteBusquedaView.as_view(), name='docente'),
    path('docentes/<int:legajo>/detalles', DocenteDetalleView.as_view(), name='detalles'),
    path('docentes/<int:legajo>/asignar-modalidad', DocenteModalidadView.as_view(), name='asignar-modalidad'),
    path('docentes/<int:legajo>/asignar-tareas', DocenteTareasView.as_view(), name='asignar-tareas'),
    path('docentes/<int:legajo>/asignar-tareas/<int:nro_cargo>', DocenteTareasView1.as_view(), name='asignar-tareas-1'),
]