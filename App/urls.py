from django.urls import path
from .views.carga_datos import *
from .views.index import *
from .views.docente_busqueda import *
from .views.docente_detalle import *
from .views.docente_modalidad import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('docentes/', DocenteBusquedaView.as_view(), name='docente'),
    path('docentes/<int:legajo>/detalles', DocenteDetalleView.as_view(), name='docente-detalle'),
    path('docentes/<int:legajo>/asignar-modalidades', DocenteModalidadView.as_view(), name='docente-asignar-modalidad'),
]