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
def getCoordinador(request, idUsuario=None):
    infoCoordinador = Coordinador.objects.filter(id_usuario = idUsuario).first()
    serializer = CoordinadorSerializer(infoCoordinador)
    print(infoCoordinador)
    return Response(serializer.data)


@api_view(['POST'])
def postCoordinador(request):
 
    if request.method == 'POST':
        nuevaSolicitud = CoordinadorSerializer(data = request.data)
        if nuevaSolicitud.is_valid():
            nuevaSolicitud.save()
            return Response(nuevaSolicitud.data)
        return Response(nuevaSolicitud.errors)
    




@api_view(['PUT'])
def updateCoordinador(request, idUsuario=None):

    solicitud = Coordinador.objects.filter(id = idUsuario).first()
    solicitud_actualizada = CoordinadorSerializer(solicitud, data = request.data)
    if solicitud_actualizada.is_valid():
        solicitud_actualizada.save()
        return Response(solicitud_actualizada.data)
    return Response(solicitud_actualizada.errors)