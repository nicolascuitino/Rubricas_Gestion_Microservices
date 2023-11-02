from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('coordinador/<int:idUsuario>', views.getCoordinador),
    path('coordinador/', views.postCoordinador),
    path('coordinador/update/<int:idUsuario>', views.updateCoordinador),
    
]