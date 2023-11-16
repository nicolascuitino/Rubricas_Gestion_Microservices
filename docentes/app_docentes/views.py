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
def getDocente(request, idUsuario=None):
    infoDocente = Docente.objects.filter(id_usuario = idUsuario).first()
    serializer = DocenteSerializer(infoDocente)
    print(infoDocente)
    return Response(serializer.data)

@api_view(['GET'])
def getDocente_id(request, idDocente=None):
    infoDocente = Docente.objects.filter(id = idDocente).first()
    serializer = DocenteSerializer(infoDocente)
    print(infoDocente)
    return Response(serializer.data)


@api_view(['POST'])
def postDocente(request):
 
    if request.method == 'POST':
        nuevaSolicitud = DocenteSerializer(data = request.data)
        if nuevaSolicitud.is_valid():
            nuevaSolicitud.save()
            return Response(nuevaSolicitud.data)
        return Response(nuevaSolicitud.errors)
    




@api_view(['PUT'])
def updateDocente(request, idUsuario=None):

    solicitud = Docente.objects.filter(id = idUsuario).first()
    solicitud_actualizada = DocenteSerializer(solicitud, data = request.data)
    if solicitud_actualizada.is_valid():
        solicitud_actualizada.save()
        return Response(solicitud_actualizada.data)
    return Response(solicitud_actualizada.errors)