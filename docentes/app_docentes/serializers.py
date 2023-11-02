from .models import *
from rest_framework import serializers


class DocenteSerializer(serializers.ModelSerializer):
    #id_usuario = UsuariosSerializers()
    class Meta: 
        model = Docente   
        fields = ('__all__') 