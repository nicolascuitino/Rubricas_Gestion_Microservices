from .models import *
from rest_framework import serializers



#Serializer que ayuda a obtener el id del estudiante, dado su id de usuario.
class EstudianteSerializer(serializers.ModelSerializer):
    #id_usuario = UsuariosSerializers()
    class Meta: 
        model = Estudiante   
        fields = ('id','rut','dig_verificador','id_usuario','id_planEstudio','id_semestreIngreso')  