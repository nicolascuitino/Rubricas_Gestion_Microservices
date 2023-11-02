from asyncio.windows_events import NULL
from django.conf import settings
from django.db import models
from django.core.validators import MinLengthValidator
from .choices import ESTADOS_SOLICITUD_CHOICES

# Create your models here.

class Solicitud_Revision(models.Model):
    motivo = models.TextField(blank = False)
    anterior_nota = models.DecimalField(max_digits = 2, decimal_places = 1, null = True, blank=True)
    actual_nota = models.DecimalField(max_digits = 2, decimal_places = 1, null = True)
    fecha_creacion = models.DateField(null = False)
    archivoAdjunto = models.FileField(blank = True, null = True)
    respuesta = models.TextField(blank = True, null = True, default = '')
    fecha_respuesta = models.DateField(blank = True, null = True, default = NULL)
    estado = models.CharField(max_length = 1, choices = ESTADOS_SOLICITUD_CHOICES, blank = False, default = '')
    id_estudiante = models.PositiveIntegerField(null = False)
    id_docente = models.PositiveIntegerField( null = False)
    id_evaluacion = models.PositiveIntegerField( null = False)
    id_calificacion = models.PositiveIntegerField(null = True)

    def __str__(self):
        return 'Solicitud de %s en la evaluacion %s' % (self.id_estudiante, self.id_evaluacion)