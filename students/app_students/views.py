from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
import requests

# Create your views here.
def hello(request):
    return HttpResponse("Hola mundo")

@api_view(['GET'])
def getEstudiante(request, idUsuario=None):
    infoEstudiante = Estudiante.objects.filter(id_usuario = idUsuario).first()
    serializer = EstudianteSerializer(infoEstudiante)
    print(infoEstudiante)
    return Response(serializer.data)


@api_view(['POST'])
def postEstudiante(request):
 

    if request.method == 'POST':
        nuevaSolicitud = EstudianteSerializer(data = request.data)
        if nuevaSolicitud.is_valid():
            nuevaSolicitud.save()
            return Response(nuevaSolicitud.data)
        return Response(nuevaSolicitud.errors)
    

@api_view(http_method_names=["GET"])
def get_semestre(request, idSemestre):
	

	

	#for product in request.data["products_id"]:
	response = requests.get("http://127.0.0.1:8003/semestre/%s" % idSemestre).json()
	print(response)
		

		#order.items.append({
		#	"item_name": response[0]["name"],
	    #		"item_description": response[0]["description"],
		#	"item_price": response[0]["price"],
		#})
	

	return Response(response)


@api_view(['PUT'])
def updateEstudiante(request, idUsuario=None):

    solicitud = Estudiante.objects.filter(id = idUsuario).first()
    solicitud_actualizada = EstudianteSerializer(solicitud, data = request.data)
    if solicitud_actualizada.is_valid():
        solicitud_actualizada.save()
        return Response(solicitud_actualizada.data)
    return Response(solicitud_actualizada.errors)

@api_view(['GET'])
def getAllEstudiantes(request):
    infoEstudiante = Estudiante.objects.all()
    serializer = EstudianteSerializer(infoEstudiante, many = True)
    print(infoEstudiante)
    return Response(serializer.data)

