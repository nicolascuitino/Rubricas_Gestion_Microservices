from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('estudiante/<int:idUsuario>', views.getEstudiante),
    path('estudiante/all', views.getAllEstudiantes),
    path('estudiante/', views.postEstudiante),
    path('estudiante/update/<int:idUsuario>', views.updateEstudiante),
    
]