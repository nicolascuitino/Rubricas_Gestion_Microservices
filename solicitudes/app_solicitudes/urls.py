from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello),
    path('solicitudes', views.getSolicitud_All),
    path('solicitud_I/<int:idUsuario>', views.getSolicitud_id),
    path('solicitud_E/<int:idUsuario>', views.getSolicitud_Estudiante),
    path('solicitud_C/<int:id>', views.getSolicitud_Calificacion),
    path('solicitud_D/<int:idUsuario>', views.getSolicitud_Docente),
    path('solicitud_EE/<int:idEstudiante>/<int:idEvaluacion>', views.getSolicitud_Estudiante_Evaluacion),
    path('add/solicitud', views.postSolicitud),
    path('solicitud/update/<int:idSolicitud>', views.updateSolicitud),
]