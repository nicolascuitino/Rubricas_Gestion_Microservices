from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator

# Create your models here.

class Estudiante(models.Model):
    rut = models.PositiveIntegerField(blank = False, null = True)
    dig_verificador = models.CharField(max_length = 1, blank = False, null = True)
    id_usuario = models.PositiveIntegerField( null = True, blank = True)
    id_planEstudio = models.PositiveIntegerField( null = True, blank = True)
    id_semestreIngreso = models.PositiveIntegerField( null = True, blank = True)

    def __str__(self):
        return '%s Rut: %s-%s' % (self.id_usuario, self.rut, self.dig_verificador)
    

