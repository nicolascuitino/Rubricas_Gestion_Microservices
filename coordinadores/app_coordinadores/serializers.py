from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User, Group
import requests


# Serializer que ayuda a obtener el id del coordinador, dado su id de usuario.
#class CoordinadorSerializer(serializers.Serializer):
#    id_usuario = UsuariosSerializers()
#    id = serializers.IntegerField()
#    rut = serializers.IntegerField()
#    dig_verificador = serializers.CharField()
#    class Meta:
#        fields = ('id', 'rut', 'dig_verificador', 'id_usuario')

class CoordinadorSerializer(serializers.ModelSerializer):
    #id_usuario = UsuariosSerializers()
    class Meta: 
        model = Coordinador   
        fields = ('__all__') 


#Serializers del proyecto original

class OnlySolicitudSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    anterior_nota = serializers.DecimalField(max_digits = 2, decimal_places = 1)
    actual_nota = serializers.DecimalField(max_digits = 2, decimal_places = 1, allow_null = True)
    fecha_creacion = serializers.DateField(allow_null = False)
    archivoAdjunto = serializers.FileField(allow_null = True)
    respuesta = serializers.CharField(allow_blank = True, allow_null = True, default = '')
    fecha_respuesta = serializers.DateField( allow_null = True)
    estado = serializers.CharField(max_length = 1, allow_blank = False, default = '')
    id_estudiante = serializers.IntegerField(allow_null = False)
    id_docente = serializers.IntegerField( allow_null = False)
    id_evaluacion = serializers.IntegerField( allow_null = False)
    id_calificacion = serializers.IntegerField(allow_null = True)
   
    class Meta:
        fields = '__all__'

class UsuariosSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RolesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class DocenteSerializer(serializers.Serializer):
    #id_usuario = UsuariosSerializers()
    id = serializers.IntegerField()
    rut = serializers.IntegerField()
    dig_verificador = serializers.CharField()

    class Meta:
        fields = ('id', 'rut', 'dig_verificador', 'id_usuario')

class CoordinadorSerializers(serializers.ModelSerializer):
    #id_usuario = UsuariosSerializers()
    class Meta:
        model = Coordinador
        fields = '__all__'


class TipoEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Evaluacion
        fields = '__all__'

class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura      
        fields = '__all__' 

class CoordinacionSeccionSerializer(serializers.ModelSerializer):
    id_asignatura = AsignaturaSerializer()
    class Meta:
        model = Coordinacion_Seccion      
        fields = ('id', 'coordinacion','seccion', 'bloques_horario', 'id_asignatura') 

class CoordinacionDocenteSerializer(serializers.ModelSerializer):
   
    id_coordinacion = CoordinacionSeccionSerializer()
    class Meta:
        model = Coordinacion_Docente    
        fields = ('id', 'id_coordinacion')
    
    

# Serializer modificado por Miguel. Para utilizarlo en las evaluaciones que tiene un curso.       
class EvaluacionSerializer(serializers.ModelSerializer):
    id_coordinacion = CoordinacionSeccionSerializer()
    id_tipoEvaluacion = TipoEvaluacionSerializer()
    #id_docente = DocenteSerializer()
    
    id_docente = serializers.SerializerMethodField()

    class Meta:
        model = Evaluacion
        fields = ('id', 'nombre', 'fechaEvActual', 'fechaEntrega', 'ponderacion', 'estado', 'obs_general', 'adjunto', 'id_tipoEvaluacion', 'id_docente', 'id_coordinacion')

    def get_id_docente(self, object):
        docente = requests.get("http://127.0.0.1:8001/docente_id/%s" % object.id_docente).json()
        return DocenteSerializer(docente).data

    #def get_id_docente(self, object):
    #    estudiante = requests.get("http://127.0.0.1:8000/estudiante/%s" % object.id_estudiante).json()
    #    return estudiante

# Serializer exclusivo para agregar evaluaciones.
class PostEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = '__all__'
#Serializer que ayuda a obtener el id del estudiante, dado su id de usuario.
class EstudianteSerializer(serializers.Serializer):
    #id_usuario = UsuariosSerializers()
    id = serializers.IntegerField()
    rut = serializers.IntegerField()
    dig_verificador = serializers.CharField()
    class Meta:   
        fields = ('id','rut','dig_verificador','id_usuario')  


    


# Modelo: Calificación -------------------------------------------------------
class CalificacionSerializer(serializers.ModelSerializer):
    id_evaluacion = EvaluacionSerializer()
    id_estudiante = serializers.SerializerMethodField()
    class Meta:
        model = Calificacion      
        fields = ('id', 'nota', 'fecha_entrega', 'obs_privada', 'adjunto' ,'id_evaluacion', 'id_estudiante')  
    
    def get_id_estudiante(self, object):
        estudiante = requests.get("http://127.0.0.1:8000/estudiante_id/%s" % object.id_estudiante).json()
        return EstudianteSerializer(estudiante).data
    


    

class CalificacionEspecificaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion      
        fields = '__all__'
# -----------------------------------------------------------------------------
#Problema en incluir id_estudiante y docente al utilizarse con many=TRUE
class SolicitudSerializer(serializers.Serializer):
    #id_evaluacion = EvaluacionSerializer()
    #id_estudiante = EstudianteSerializer()
    #id_estudiante = serializers.SerializerMethodField()
    #id_docente = DocenteSerializer()
    #id_docente = serializers.SerializerMethodField()
    #id_calificacion = CalificacionEspecificaSerializer()

    #Solicitud
    id = serializers.IntegerField()
    anterior_nota = serializers.DecimalField(max_digits = 2, decimal_places = 1)
    actual_nota = serializers.DecimalField(max_digits = 2, decimal_places = 1, allow_null = True)
    fecha_creacion = serializers.DateField(allow_null = False)
    archivoAdjunto = serializers.FileField(allow_null = True)
    respuesta = serializers.CharField(allow_blank = True, allow_null = True, default = '')
    fecha_respuesta = serializers.DateField( allow_null = True)
    estado = serializers.CharField(max_length = 1, allow_blank = False, default = '')
    class Meta:
       
        fields = '__all__'
    
    def get_id_estudiante(self, object):
        estudiante = requests.get("http://127.0.0.1:8000/estudiante_id/%s" % object.id_estudiante).json()
        return EstudianteSerializer(estudiante).data
    
    def get_id_docente(self, object):
        docente = requests.get("http://127.0.0.1:8001/docente_id/%s" % object.id_docente).json()
        return DocenteSerializer(docente).data

# Modificado: Se quito el comentario de id_estudiante.
class CoordinacionEstudianteSerializer(serializers.ModelSerializer):
    #id_estudiante = EstudianteSerializer()
    #id_estudiante = serializers.SerializerMethodField()
    id_coordinacion = CoordinacionSeccionSerializer()
    class Meta:
        model = Coordinacion_Estudiante    
        fields = ('promedioEstudiante', 'id_estudiante', 'id_coordinacion')
    
    def get_id_estudiante(self, object):
        estudiante = requests.get("http://127.0.0.1:8000/estudiante_id/%s" % object.id_estudiante).json()
        return EstudianteSerializer(estudiante).data

#Serializer para mostrar datos en respuesta de solicitud
class SolicitudRespuestaSerializer(serializers.Serializer):
    #id_estudiante = EstudianteSerializer()
    #id_evaluacion = EvaluacionSerializer()
    #id_calificacion = CalificacionEspecificaSerializer()
    #Solicitud

    id = serializers.IntegerField()
    anterior_nota = serializers.DecimalField(max_digits = 2, decimal_places = 1)
    actual_nota = serializers.DecimalField(max_digits = 2, decimal_places = 1, allow_null = True)
    fecha_creacion = serializers.DateField(allow_null = False)
    archivoAdjunto = serializers.FileField(allow_null = True)
    respuesta = serializers.CharField(allow_blank = True, allow_null = True, default = '')
    fecha_respuesta = serializers.DateField( allow_null = True)
    estado = serializers.CharField(max_length = 1, allow_blank = False, default = '')
    id_docente = serializers.IntegerField( allow_null = False)
    class Meta:
        
        fields = '__all__'

######################################################################################33
## Saber las secciones de un coordinador con su asignatura - 2 - Ademas de mostrar las secciones para un Jefe de carrera
class CoordinacionCoordinadorSerializer(serializers.ModelSerializer):
    id_asignatura = AsignaturaSerializer()
    class Meta:
        model = Coordinacion_Seccion      
        fields = '__all__'  
## Saber las secciones de un coordinador con su asignatura - 1
class DocenteCursoSerializer(serializers.ModelSerializer):
    id_coordinacion = CoordinacionCoordinadorSerializer()
    #id_docente = DocenteSerializer()
    id_docente = serializers.SerializerMethodField()
    class Meta:
        model = Coordinacion_Docente      
        fields = '__all__'  
    
    def get_id_docente(self, object):
        docente = requests.get("http://127.0.0.1:8001/docente_id/%s" % object.id_docente).json()
        return DocenteSerializer(docente).data


# Para obtener las solicitudes respecto a un curso - 2
class SolicitudesEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion  
        fields = ('id','id_coordinacion','nombre')  
# Para obtener las solicitudes respecto a un curso - 1 ------- ## Usado para ver la solicitudes de una asignatura de un jefe
class SolicitudesDocenteCursoSerializer(serializers.Serializer):
    #id_evaluacion = SolicitudesEvaluacionSerializer()
    #id_estudiante = EstudianteSerializer()
    #id_calificacion = CalificacionEspecificaSerializer()
    #id_docente = DocenteSerializer()

    #Solicitud
    id = serializers.IntegerField()
    anterior_nota = serializers.DecimalField(max_digits = 2, decimal_places = 1)
    actual_nota = serializers.DecimalField(max_digits = 2, decimal_places = 1, allow_null = True)
    fecha_creacion = serializers.DateField(allow_null = False)
    archivoAdjunto = serializers.FileField(allow_null = True)
    respuesta = serializers.CharField(allow_blank = True, allow_null = True, default = '')
    fecha_respuesta = serializers.DateField( allow_null = True)
    estado = serializers.CharField(max_length = 1, allow_blank = False, default = '')

    
    class Meta:
          
        fields ='__all__'  
###########################################################################################

# Obtener los planes de estudios pertenecientes a un jefe de carrera - 3
class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera  
        fields = ('id','id_jefeCarrera')  

# Obtener los planes de estudios pertenecientes a un jefe de carrera - 2
class PlanEstudioSerializer(serializers.ModelSerializer):
    id_carrera = CarreraSerializer()
    class Meta:
        model = Plan_Estudio
        fields = ('id','id_carrera')  
        
# Obtener los planes de estudios pertenecientes a un jefe de carrera - 2
class AsignaturaV2Serializer(serializers.ModelSerializer):
    id_coordinador = CoordinadorSerializers()
    class Meta:
        model = Asignatura      
        fields = '__all__'  

# Obtener los planes de estudios pertenecientes a un jefe de carrera - 1
class PlanesJefeSerializer(serializers.ModelSerializer):
    id_planEstudio = PlanEstudioSerializer()
    id_asignatura = AsignaturaV2Serializer()
    class Meta:
        model = Asignaturas_PlanEstudio  
        fields = '__all__'

class EvaluacionEspecificaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion      
        fields = '__all__'

# Modelo: Cambio_nota ---------------------------------------------------------

# Creo que este serializer está malo, ya que no se estaría considerando el 
# id_calificacion al poner all. 
class CambioNotaSerializer(serializers.ModelSerializer):
    id_calificacion = CalificacionSerializer()
    class Meta:
        model = Cambio_nota      
        fields = '__all__'

class CambioNotaEspecificaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cambio_nota      
        fields = '__all__'
# -----------------------------------------------------------------------------

# Serializer para cambios de fecha.
class CambioFechaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cambio_Fecha
        fields = '__all__'

# Serializer para cambios de fecha en el dashboard.
class CambioFechaDashboardSerializer(serializers.ModelSerializer):
    id_evaluacion = EvaluacionSerializer()
    class Meta:
        model = Cambio_Fecha
        fields = '__all__'

# Serializer de evaluación para los cambios de fecha en el dashboard.       
class EvaluacionCambioFechaSerializer(serializers.ModelSerializer):
    id_coordinacion = CoordinacionSeccionSerializer()
    id_docente = DocenteSerializer()  
    class Meta:
        model = Evaluacion
        fields = ('id_docente', 'id_coordinacion')

# Serializer para cambios de notas en  dashboard.
class CambioNotaDashboardSerializer(serializers.ModelSerializer):
    id_calificacion = CalificacionSerializer()
    class Meta:
        model = Cambio_nota
        fields = '__all__'

class CambioPonderacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cambio_Ponderacion
        fields = '__all__'

# Serializer para obtener los cambios de ponderacion segun asignatura.
class CambioPonderacionesJefe(serializers.ModelSerializer):
    id_evaluacion = EvaluacionSerializer()
    class Meta:
        model = Cambio_Ponderacion
        fields = '__all__'
        
#funcionando
class EvaluacionDocenteSerializer(serializers.ModelSerializer):
    #id_docente = DocenteSerializer()
    id_docente = serializers.SerializerMethodField()
    id_coordinacion = CoordinacionSeccionSerializer()
    class Meta:
        model = Evaluacion
        fields = '__all__'
    
    def get_id_docente(self, object):
        docente = requests.get("http://127.0.0.1:8001/docente_id/%s" % object.id_docente).json()
        return DocenteSerializer(docente).data

class CoordinacionDocenteCursoEspejoSerializer(serializers.ModelSerializer):
    #id_docente = DocenteSerializer()
    id_docente = serializers.SerializerMethodField()
    id_coordinacion = CoordinacionSeccionSerializer()
    class Meta:
        model = Coordinacion_Docente    
        fields = '__all__'
    
    def get_id_docente(self, object):
        docente = requests.get("http://127.0.0.1:8001/docente_id/%s" % object.id_docente).json()
        return DocenteSerializer(docente).data