from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *


# Create your views here.
def hello(request):
    return HttpResponse("Hola mundo")

@api_view(['GET'])
#obtiene solicitud que calce con un mismo id de solicitud
def getSolicitud_id(request, idUsuario=None):
    infoSolicitudes = Solicitud_Revision.objects.filter(id = idUsuario).first()
    serializer = OnlySolicitudSerializer(infoSolicitudes)
    print(infoSolicitudes)
    return Response(serializer.data)

@api_view(['GET'])
#obtiene solicitudes que calcen con un mismo id_estudiante
def getSolicitud_Estudiante(request, idUsuario=None):
    infoSolicitudes = Solicitud_Revision.objects.filter(id_estudiante = idUsuario)
    serializer = OnlySolicitudSerializer(infoSolicitudes, many=True)
    print(infoSolicitudes)
    return Response(serializer.data)

@api_view(['GET'])
#obtiene solicitudes que calcen con un mismo id_estudiante
def getSolicitud_Docente(request, idUsuario=None):
    infoSolicitudes = Solicitud_Revision.objects.filter(id_docente = idUsuario)
    serializer = OnlySolicitudSerializer(infoSolicitudes, many=True)
    print(infoSolicitudes)
    return Response(serializer.data)

@api_view(['GET'])
#obtiene solicitudes que calcen con un mismo id_calificacion
def getSolicitud_Calificacion(request, id=None):
    infoSolicitudes = Solicitud_Revision.objects.filter(id_calificacion = id)
    serializer = Solicitud_Revision(infoSolicitudes, many=True)
    print(infoSolicitudes)
    return Response(serializer.data)

@api_view(['GET'])
#obtiene solicitudes que calcen con un mismo id_calificacion
def getSolicitud_Estudiante_Evaluacion(request, idEstudiante=None, idEvaluacion =None):
    infoSolicitudes = Solicitud_Revision.objects.filter(id_estudiante = idEstudiante, id_evaluacion = idEvaluacion)
    serializer = OnlySolicitudSerializer(infoSolicitudes, many= "true")
    print(infoSolicitudes)
    return Response(serializer.data)

@api_view(['GET'])
#obtiene solicitudes que calcen con un mismo id_calificacion
def getSolicitud_All(request):
    infoSolicitudes = Solicitud_Revision.objects.all()
    serializer = OnlySolicitudSerializer(infoSolicitudes, many= "true")
    print(infoSolicitudes)
    return Response(serializer.data)


@api_view(['POST'])
def postSolicitud(request):
 
    if request.method == 'POST':
        nuevaSolicitud = OnlySolicitudSerializer(data = request.data)
        if nuevaSolicitud.is_valid():
            nuevaSolicitud.save()
            return Response(nuevaSolicitud.data)
        return Response(nuevaSolicitud.errors)
    




@api_view(['PUT'])
def updateSolicitud(request, idSolicitud=None):

    solicitud = Solicitud_Revision.objects.filter(id = idSolicitud).first()
    solicitud_actualizada = Solicitud_Revision(solicitud, data = request.data)
    if solicitud_actualizada.is_valid():
        solicitud_actualizada.save()
        return Response(solicitud_actualizada.data)
    return Response(solicitud_actualizada.errors)
