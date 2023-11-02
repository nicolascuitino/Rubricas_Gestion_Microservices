from django.db import models

# Create your models here.

class Coordinador(models.Model):
    rut = models.PositiveIntegerField(blank = False, null = True)
    dig_verificador = models.CharField(max_length = 1, blank = False, null = True)
    id_usuario = models.ForeignKey( null = True, blank = True)

    def __str__(self):
        return '%s Rut: %s-%s' % (self.id_usuario, self.rut, self.dig_verificador)
