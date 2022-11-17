from django.db import models

class Cargas_Extras(models.Model):
    nombre = models.CharField(max_length=100)
    horas = models.IntegerField()
    
    def __str__(self):
        return self.nombre
    
 
class Resolucion(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    documento = models.ImageField(upload_to='pdf')
    
    def __str__(self):
        return self.nombre
