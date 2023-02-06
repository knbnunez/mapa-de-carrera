from django.urls import path
from .views.views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('docente/<int:legajo>/', DocenteView.as_view(), name='docente'),
]