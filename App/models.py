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
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    

class Modalidad(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    
class Dedicacion(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    
 class Localidad(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
 
class Periodo_Electivo(models.Model):
    nombre = models.CharField(max_length=100)
    desde = models.DateField()
    hasta = models.DateField()
    
    def __str__(self):
        return self.nombre
    
class Instituto(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    id_instituto = models.ForeignKey(Instutito, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.nombre
    
    
class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    id_carrera = models.ManyToManyField(Carrera)
   
    def __str__(self):
        return self.nombre

