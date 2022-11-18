from django.urls import path
from App.views.views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
]