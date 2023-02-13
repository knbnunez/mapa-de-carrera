from django.urls import path
from .views.views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('docente/', DocenteBusquedaView.as_view(), name='buscadocente'),
    path('docente/<int:legajo>/', DocenteView.as_view(), name='docente'),
]