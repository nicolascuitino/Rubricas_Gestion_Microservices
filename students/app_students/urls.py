from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('estudiante/<int:idUsuario>', views.getEstudiante),
    path('estudiante_id/<int:idEstudiante>', views.getEstudiante_id),
    path('estudiante/all', views.getAllEstudiantes),
    path('estudiante/', views.postEstudiante),
    path('estudiante/update/<int:idUsuario>', views.updateEstudiante),
    
]