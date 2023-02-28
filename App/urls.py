from django.urls import path
from .views.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('docentes/', DocenteBusquedaView.as_view(), name='buscadocente'),
    path('docentes/<int:legajo>/', DocenteDetalleView.as_view(), name='docente'),
    path('docentes/<int:legajo>/asignar-modalidades', DocenteModalidadView.as_view(), name='docente-modalidad'),
]