from django.urls import include, path

from .views.docente_historico import *
from .views.index import *
from .views.docente_busqueda import *
from .views.docente_detalle import *
from .views.docente_modalidad import *
from .views.docente_tareas import *
from .views.docente_comision import *
from .views.docente_carga_horaria import *
from .views.login import *
from .views.docente_carga_horaria import *
from .views.general_sobrecarga_deficit import *
from .views.general_comisiones_sin_asignar import *

from django.conf import settings
from django.conf.urls.static import static
from social_django.urls import urlpatterns as social_django_urls


urlpatterns = [
    # path('', IndexView.as_view(), name='index'),    
    path('', login_view, name='login'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/login/', cargar_base, name='cargar-base'), 
    # path('accounts/login/', DocenteBusquedaView.as_view(), name='docente'), 
    path('cargar-base/', cargar_base, name='cargar-base'),
    #
    path('docentes/', DocenteBusquedaView.as_view(), name='docente'),
    path('carga-horaria/', DocenteCargaHorariaView.as_view(), name='docente-carga'),
    path('docentes/<int:legajo>/detalles', DocenteDetalleView.as_view(), name='docente-detalle'),
    path('docentes/<int:legajo>/historico', DocenteHistoricoView.as_view(), name='docente-historico'),
    path('docentes/<int:legajo>/asignar-modalidad', DocenteModalidadView.as_view(), name='docente-asignar-modalidad'),
    path('docentes/<int:legajo>/asignar-tareas', DocenteTareasView.as_view(), name='docente-asignar-tareas'),
    path('docentes/<int:legajo>/asignar-comision', DocenteComisionView.as_view(), name='docente-asignar-comision'),
    #
    path('sobrecarga-deficit/', GeneralSobrecargaDeficitView.as_view(), name='sobrecarga-deficit'),
    path('comisiones-sin-asignar/', GeneralComisionesSinAsignar.as_view(), name='comisiones-sin-asignar')
]

urlpatterns += social_django_urls

# Ruta para servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
