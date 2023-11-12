import datetime
from distutils.log import error
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from django.contrib.auth.models import User, Group
from datetime import date
from django.db.models import Q
import requests

#------Metodos de JefeCarrera------
@api_view(['GET'])
def getJefeCarrera(request, idUsuario=None):
    infoJefe = Jefe_Carrera.objects.filter(id_usuario = idUsuario).first()
    serializer = JefeCarreraSerializer(infoJefe)
    print(infoJefe)
    return Response(serializer.data)


@api_view(['POST'])
def postJefeCarrera(request):
 
    if request.method == 'POST':
        nuevaSolicitud = JefeCarreraSerializer(data = request.data)
        if nuevaSolicitud.is_valid():
            nuevaSolicitud.save()
            return Response(nuevaSolicitud.data)
        return Response(nuevaSolicitud.errors)
    




@api_view(['PUT'])
def updateJefeCarrera(request, idUsuario=None):

    solicitud = Jefe_Carrera.objects.filter(id = idUsuario).first()
    solicitud_actualizada = JefeCarreraSerializer(solicitud, data = request.data)
    if solicitud_actualizada.is_valid():
        solicitud_actualizada.save()
        return Response(solicitud_actualizada.data)
    return Response(solicitud_actualizada.errors)

#------Fin Metodos de JefeCarrera------


#------Metodos de Subdirector_Docente------
@api_view(['GET'])
def getSubdirector_Docente(request, idUsuario=None):
    infoSubdirector_Docente = Subdirector_Docente.objects.filter(id_usuario = idUsuario).first()
    serializer = Subdirector_DocenteSerializer(infoSubdirector_Docente)
    print(infoSubdirector_Docente)
    return Response(serializer.data)


@api_view(['POST'])
def postSubdirector_Docente(request):
 
    if request.method == 'POST':
        nuevaSolicitud = Subdirector_DocenteSerializer(data = request.data)
        if nuevaSolicitud.is_valid():
            nuevaSolicitud.save()
            return Response(nuevaSolicitud.data)
        return Response(nuevaSolicitud.errors)
    




@api_view(['PUT'])
def updateSubdirector_Docente(request, idUsuario=None):

    solicitud = Subdirector_Docente.objects.filter(id = idUsuario).first()
    solicitud_actualizada = Subdirector_DocenteSerializer(solicitud, data = request.data)
    if solicitud_actualizada.is_valid():
        solicitud_actualizada.save()
        return Response(solicitud_actualizada.data)
    return Response(solicitud_actualizada.errors)

#------Fin Metodos de JefeCarrera------

#------Metodos de Vicedecano_Docencia------
@api_view(['GET'])
def getVicedecano_Docencia(request, idUsuario=None):
    infoVicedecano_Docencia = Vicedecano_Docencia.objects.filter(id_usuario = idUsuario).first()
    serializer = Vicedecano_DocenciaSerializer(infoVicedecano_Docencia)
    print(infoVicedecano_Docencia)
    return Response(serializer.data)


@api_view(['POST'])
def postVicedecano_Docencia(request):
 
    if request.method == 'POST':
        nuevaSolicitud = Vicedecano_DocenciaSerializer(data = request.data)
        if nuevaSolicitud.is_valid():
            nuevaSolicitud.save()
            return Response(nuevaSolicitud.data)
        return Response(nuevaSolicitud.errors)
    




@api_view(['PUT'])
def updateVicedecano_Docencia(request, idUsuario=None):

    solicitud = Vicedecano_Docencia.objects.filter(id = idUsuario).first()
    solicitud_actualizada = Vicedecano_DocenciaSerializer(solicitud, data = request.data)
    if solicitud_actualizada.is_valid():
        solicitud_actualizada.save()
        return Response(solicitud_actualizada.data)
    return Response(solicitud_actualizada.errors)

#------Fin Metodos de JefeCarrera------