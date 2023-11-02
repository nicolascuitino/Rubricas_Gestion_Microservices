from .models import *
from rest_framework import serializers


class CoordinadorSerializer(serializers.ModelSerializer):
    #id_usuario = UsuariosSerializers()
    class Meta: 
        model = Coordinador   
        fields = ('__all__') 