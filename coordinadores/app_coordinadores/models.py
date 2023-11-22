from django.db import models
from django.core.validators import MinLengthValidator
#from asyncio.windows_events import NULL
from django.conf import settings
from .choices import COMPONENTES_CHOICES, ESTADOS_EVALUACION_CHOICES, ESTADOS_SOLICITUD_CHOICES, SEMESTRES_CHOICES

# Create your models here.

class Tipos(models.Model):
    nombre = models.CharField(max_length = 40)

    class Meta:
        abstract = True

# -----------------------------------------------------------------------------

class Coordinador(models.Model):
    rut = models.PositiveIntegerField(blank = False, null = True)
    dig_verificador = models.CharField(max_length = 1, blank = False, null = True)
    id_usuario = models.PositiveIntegerField( null = True, blank = True)

    def __str__(self):
        return '%s Rut: %s-%s' % (self.id_usuario, self.rut, self.dig_verificador)
    

#coordinacion
class Facultad(models.Model):
    nombre = models.CharField(max_length = 100, blank = False)
    siglas = models.CharField(max_length = 10, blank = True)
    id_vicedecano = models.PositiveIntegerField( blank = False , null = False)

    def __str__(self):
        return self.nombre
#coordinacion
class Departamento(models.Model):
    nombre = models.CharField(max_length = 50, blank = False)
    id_subdirector = models.PositiveIntegerField( blank = False , null = False)
    id_facultad = models.ForeignKey(Facultad, blank = False, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.nombre
#coordinacion
class Carrera(models.Model):
    nombre = models.CharField(max_length = 100, blank = False)
    id_jefeCarrera = models.PositiveIntegerField( blank = False, null = False)
    id_departamento = models.ForeignKey(Departamento, blank = False, null = False, on_delete = models.CASCADE)

    def __str__(self):
        return self.nombre
#coordinacion
class Plan_Estudio(models.Model):
    codigo = models.CharField(max_length = 10, blank = False)
    year_creacion = models.CharField(max_length = 4, validators = [MinLengthValidator(4)])
    id_carrera = models.ForeignKey(Carrera, blank = False, null = False, on_delete = models.CASCADE)

    def __str__(self):
        return '%s de %s' % (self.codigo, self.id_carrera)
#coordinacion
class Tipo_Asignatura(Tipos):

    def __str__(self):
        return self.nombre
#coordinacion
class Asignatura(models.Model):
    nombre = models.CharField(max_length = 80, blank = False)
    codigo = models.CharField(max_length = 20, blank = False)
    nivel = models.PositiveSmallIntegerField(blank = True, null = True)
    componente = models.CharField(max_length = 1, choices = COMPONENTES_CHOICES, blank = False)
    isMBI = models.BooleanField(default = False)
    isAutogestionada = models.BooleanField(default = False)
    id_tipoAsignatura = models.ForeignKey(Tipo_Asignatura, blank = True, null = True, on_delete = models.CASCADE)
    id_coordinador = models.PositiveIntegerField( blank = True, null = True)

    def __str__(self):
        return '%s - %s (%s)' % (self.nombre, self.codigo, self.componente)
#coordinacion
class Asignaturas_PlanEstudio(models.Model):
    id_asignatura = models.ForeignKey(Asignatura, blank = False, null = False, on_delete = models.CASCADE)
    id_planEstudio = models.ForeignKey(Plan_Estudio, blank = False, null = False, on_delete = models.CASCADE)
#coordinacion
class Semestre(models.Model):
    year = models.PositiveSmallIntegerField(null = False)
    semestre = models.IntegerField(choices = SEMESTRES_CHOICES, blank = False)
    isActual = models.BooleanField(default = False)

    def __str__(self):
        return 'Semestre %s/%s' % (self.year, self.semestre)
#coordinacion
class Coordinacion_Seccion(models.Model):
    coordinacion = models.CharField(max_length = 1, blank = False)
    seccion = models.PositiveSmallIntegerField(blank = False)
    isActive = models.BooleanField(default = False)
    bloques_horario = models.CharField(max_length = 16, blank = False)
    id_semetre = models.ForeignKey(Semestre, null = False, on_delete = models.CASCADE)
    id_asignatura = models.ForeignKey(Asignatura, null = False, on_delete = models.CASCADE)

    def __str__(self):
        return '%s - %s sección %s-%s (%s)' % (self.id, self.id_asignatura, self.coordinacion, self.seccion, self.bloques_horario)
#No definida
class Estadistica_Curso(models.Model):
    promedio_general = models.DecimalField(max_digits = 4, decimal_places = 3)
    mejor_nota = models.DecimalField(max_digits = 4, decimal_places = 3)
    peor_nota = models.DecimalField(max_digits = 4, decimal_places = 3)
    desviacionEstandar = models.DecimalField(max_digits = 4, decimal_places = 3)
    id_coordinacion = models.ForeignKey(Coordinacion_Seccion, null = False, on_delete = models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add = True)
#No definida pero puede estar en coordinadores
class Coordinacion_Docente(models.Model):
    id_docente = models.PositiveIntegerField(null = False)
    id_coordinacion = models.ForeignKey(Coordinacion_Seccion, null = False, on_delete = models.CASCADE)
    

#No definida pero puede estar en coordinadores
class Coordinacion_Estudiante(models.Model):
    promedioEstudiante = models.DecimalField(max_digits = 2, decimal_places = 1, null = True, blank = True)
    id_estudiante = models.PositiveIntegerField(null = False)
    id_coordinacion = models.ForeignKey(Coordinacion_Seccion, null = False, on_delete = models.CASCADE)

#Definida en gestion de rubricas
class Tipo_Evaluacion(Tipos):
    
    def __str__(self):
        return self.nombre
#Definida en gestion de rubricas
class Evaluacion(models.Model):
    nombre = models.CharField(max_length = 40, blank = False)
    fechaEvActual = models.DateField(null = False)
    fechaEntrega = models.DateField(null = True, blank = True)
    ponderacion = models.DecimalField(max_digits = 4, decimal_places = 3, null = False)
    estado = models.CharField(max_length = 1, choices = ESTADOS_EVALUACION_CHOICES, blank = False)
    obs_general = models.TextField(blank = True, default = '')
    adjunto = models.FileField(upload_to='observaciones/evaluacion/', blank = True, null = True)
    id_tipoEvaluacion = models.ForeignKey(Tipo_Evaluacion, null = True, on_delete = models.CASCADE)
    id_docente = models.PositiveIntegerField( null = False)
    id_coordinacion = models.ForeignKey(Coordinacion_Seccion, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return '%s de %s' % (self.nombre, self.id_coordinacion)
#Definida en gestion de rubricas
class Cambio_Ponderacion(models.Model):
    ponderacionAnterior = models.DecimalField(max_digits = 4, decimal_places = 3, null = False)
    ponderacionNueva = models.DecimalField(max_digits = 4, decimal_places = 3, null = False)
    motivo = models.TextField(blank = False)
    fecha_cambio = models.DateField(null = True)
    id_evaluacion = models.ForeignKey(Evaluacion, null = False, on_delete = models.CASCADE)

#Definida en gestion de rubricas
class Cambio_Fecha(models.Model):
    fechaAnterior = models.DateField(null = False)
    fechaNueva = models.DateField(null = False)
    motivo = models.TextField(blank = False)
    fecha_cambio = models.DateField(null = True)
    id_evaluacion = models.ForeignKey(Evaluacion, null = False, on_delete = models.CASCADE)

#Definida en gestion de rubricas
class Calificacion(models.Model):
    nota = models.DecimalField(max_digits = 2, decimal_places = 1, null = True, blank = True)
    fecha_entrega = models.DateField(null = True, blank = True)
    obs_privada = models.TextField(blank = True, default = '')
    adjunto = models.FileField(upload_to='observaciones/estudiantes/', blank = True, null = True)
    id_estudiante = models.PositiveIntegerField(null = False)
    id_evaluacion = models.ForeignKey(Evaluacion, null = False, on_delete = models.CASCADE)

    def __str__(self):
        return 'Nota %s de %s de la ev %s' % (self.nota, self.id_estudiante, self.id_evaluacion)

#Ya definida en solicitudes
#class Solicitud_Revision(models.Model):
#    motivo = models.TextField(blank = False)
#   anterior_nota = models.DecimalField(max_digits = 2, decimal_places = 1, null = True, blank=True)
#    actual_nota = models.DecimalField(max_digits = 2, decimal_places = 1, null = True)
#   fecha_creacion = models.DateField(null = False)
#    archivoAdjunto = models.FileField(blank = True, null = True)
#    respuesta = models.TextField(blank = True, null = True, default = '')
#    fecha_respuesta = models.DateField(blank = True, null = True, default = NULL)
#    estado = models.CharField(max_length = 1, choices = ESTADOS_SOLICITUD_CHOICES, blank = False, default = '')
#    id_estudiante = models.PositiveIntegerField(null = False)
#    id_docente = models.PositiveIntegerField( null = False)
#    id_evaluacion = models.ForeignKey(Evaluacion, null = False, on_delete = models.CASCADE)
#    id_calificacion = models.ForeignKey(Calificacion,null = True, on_delete = models.CASCADE)

#    def __str__(self):
#       return 'Solicitud de %s en la evaluacion %s' % (self.id_estudiante, self.id_evaluacion)

#No definida pero podria estar en gestion de rubricas
class Cambio_nota(models.Model):
    anterior_nota = models.DecimalField(max_digits = 2, decimal_places = 1, null = False)
    actual_nota = models.DecimalField(max_digits = 2, decimal_places = 1, null = False)
    fecha_cambio = models.DateField(null = True)
    motivo = models.TextField(blank = False)
    id_calificacion = models.ForeignKey(Calificacion, null = False, on_delete = models.CASCADE)


# -----------------------------
# Modelos de otros microservicios

class Solicitud_Revision(models.Model):
    id = models.PositiveIntegerField(primary_key=True,blank = False)
    motivo = models.TextField(blank = False)
    anterior_nota = models.DecimalField(max_digits = 2, decimal_places = 1, null = True, blank=True)
    actual_nota = models.DecimalField(max_digits = 2, decimal_places = 1, null = True)
    fecha_creacion = models.DateField(null = False)
    archivoAdjunto = models.FileField(blank = True, null = True)
    respuesta = models.TextField(blank = True, null = True, default = '')
    fecha_respuesta = models.DateField(blank = True, null = True)
    estado = models.CharField(max_length = 1, choices = ESTADOS_SOLICITUD_CHOICES, blank = False, default = '')
    id_estudiante = models.PositiveIntegerField(null = False)
    id_docente = models.PositiveIntegerField( null = False)
    id_evaluacion = models.PositiveIntegerField( null = False)
    id_calificacion = models.PositiveIntegerField(null = True)

    class Meta:
        managed = False

    def __str__(self):
        return 'Solicitud de %s en la evaluacion %s' % (self.id_estudiante, self.id_evaluacion)

    
