from .models import *
from rest_framework import serializers


class OnlySolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud_Revision
        fields = '__all__'


