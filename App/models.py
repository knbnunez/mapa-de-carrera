from django.db import models


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

class Docente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.IntegerField()
    DNI = models.IntegerField()
    legajo = models.IntegerField()
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
class Coordinador(models.Model):
    id_docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    id_instituto = models.ForeignKey(Instituto, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

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
    

class Tipo(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    
class franja_Horaria(models.Model):
    nombre = models.CharField(max_length=100)
    dia = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
    
class Periodo_Electivo(models.Model):
    nombre = models.CharField(max_length=100)
    desde = models.DateField()
    hasta = models.DateField()
    
    def __str__(self):
        return self.nombre
    


 class Comision(models.Model):
    nombre = models.CharField(max_length=100)
    id_materia = models.ManyToManyField(Materia)
    id_periodo_electivo = models.ForeignKey(Periodo_Electivo, on_delete=models.CASCADE)
    id_franja_horaria = models.ManyToManyField(Franja_Horaria, on_delete=models.CASCADE)
    id_localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
