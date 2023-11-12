from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #URLS de Vicedecano_Docencia
 
    path('vicedecano_docencia/<int:idUsuario>', views.getVicedecano_Docencia),
    path('vicedecano_docencia/', views.postVicedecano_Docencia),
    path('vicedecano_docencia/update/<int:idUsuario>', views.updateVicedecano_Docencia),

    #URLS de Subdirector_Docente
 
    path('subdirector_docente/<int:idUsuario>', views.getSubdirector_Docente),
    path('subdirector_docente/', views.postSubdirector_Docente),
    path('subdirector_docente/update/<int:idUsuario>', views.updateSubdirector_Docente),

    #URLS de Vicedecano_Docencia

    path('jefe_carrera/<int:idUsuario>', views.getJefeCarrera),
    path('jefe_carrera/', views.postJefeCarrera),
    path('Jefe_carrera/update/<int:idUsuario>', views.updateJefeCarrera),
 
    
] 