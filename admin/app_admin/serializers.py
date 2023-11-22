from dataclasses import field
from pyexpat import model
from psycopg2 import Date
from rest_framework import serializers
from .models import *
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group

class UsuariosSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Serializer que ayuda a obtener el id del jefe de carrera, dado su id de usuario.
class JefeCarreraSerializer(serializers.ModelSerializer):
    #id_usuario = UsuariosSerializers()
    class Meta:
        model = Jefe_Carrera  
        fields = ('id', 'rut', 'dig_verificador', 'id_usuario')

class Subdirector_DocenteSerializer(serializers.ModelSerializer):
    #id_usuario = UsuariosSerializers()
    class Meta:
        model = Subdirector_Docente  
        fields = ('id', 'rut', 'dig_verificador', 'id_usuario')

class Vicedecano_DocenciaSerializer(serializers.ModelSerializer):
    id_usuario = UsuariosSerializers()
    class Meta:
        model = Vicedecano_Docencia  
        fields = ('id', 'rut', 'dig_verificador', 'id_usuario')

