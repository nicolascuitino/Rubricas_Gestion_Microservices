from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('docente/<int:idUsuario>', views.getDocente),
    path('docente_id/<int:idDocente>', views.getDocente_id),
    path('docente/', views.postDocente),
    path('docente/update/<int:idUsuario>', views.updateDocente),
    
]