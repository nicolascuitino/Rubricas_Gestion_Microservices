from asyncio.windows_events import NULL
from django.conf import settings
from django.db import models
from .choices import COMPONENTES_CHOICES, ESTADOS_EVALUACION_CHOICES, ESTADOS_SOLICITUD_CHOICES, SEMESTRES_CHOICES

# Create your models here.


class Vicedecano_Docencia(models.Model):
    rut = models.PositiveIntegerField(blank = False, null = True)
    dig_verificador = models.CharField(max_length = 1, blank = False, null = True)
    id_usuario = models.PositiveIntegerField( null = True, blank = True)

    def __str__(self):
        return '%s Rut: %s-%s' % (self.id_usuario, self.rut, self.dig_verificador)

class Subdirector_Docente(models.Model):
    rut = models.PositiveIntegerField(blank = False, null = True)
    dig_verificador = models.CharField(max_length = 1, blank = False, null = True)
    id_usuario = models.PositiveIntegerField( null = True, blank = True)

    def __str__(self):
        return '%s Rut: %s-%s' % (self.id_usuario, self.rut, self.dig_verificador)

class Jefe_Carrera(models.Model):
    rut = models.PositiveIntegerField(blank = False, null = True)
    dig_verificador = models.CharField(max_length = 1, blank = False, null = True)
    id_usuario = models.PositiveIntegerField( null = True, blank = True)

    def __str__(self):
        return '%s Rut: %s-%s' % (self.id_usuario, self.rut, self.dig_verificador)



