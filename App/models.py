from django.db import models


class Instituto(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    id_instituto = models.ForeignKey(Instituto, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.nombre
    
    
class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    id_carrera = models.ManyToManyField(Carrera)
   
    def __str__(self):
        return self.nombre


class Docente(models.Model):
    numero_documento = models.IntegerField()
    legajo = models.IntegerField()
    nombre_apellido = models.CharField(max_length=240)
    apellido = models.IntegerField()
    fecha_ingreso = models.DateField()
    fecha_jubilacion = models.DateField(null=True)
    correo_electronico = models.EmailField(null=False)

    def __str__(self):
        return self.nombre
    

# Se eleminó la clase Coordinador. La distinción será arreglada con roles dentro de la aplicación


class Cargas_Extras(models.Model):
    nombre = models.CharField(max_length=100)
    horas = models.IntegerField()
    
    def __str__(self):
        return self.nombre
    
 
class Resolucion(models.Model):
    nombre = models.CharField(max_length=100)
    # De las dudas: las fechas son las mismas que podemos obtener del endpoint de /agentes/{legajo}/cargos ???
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
    
    
class Modalidad_Dedicacion(models.Model):
    id_modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    id_dedicacion = models.ForeignKey(Dedicacion, on_delete=models.CASCADE)
    horas_minimas = models.IntegerField()
    horas_maximas = models.IntegerField()
    
    
class Localidad(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    

class Tipo(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    
class Franja_Horaria(models.Model):
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
    id_franja_horaria = models.ManyToManyField(Franja_Horaria)
    id_localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
    
class Cargo(models.Model):
    id_docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    id_resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE)
    id_dependencia_desempeno = models.ForeignKey(Instituto, on_delete=models.CASCADE, related_name='cargo_desmpeno')
    id_dependencia_designacion = models.ForeignKey(Instituto, on_delete=models.CASCADE, related_name='cargo_designacion')
    id_dedicacion = models.ForeignKey(Dedicacion, on_delete=models.CASCADE)
    id_cargas_extras = models.ManyToManyField(Cargas_Extras)
    id_franja_horaria = models.ManyToManyField(Franja_Horaria)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    # Vienen de la API
    fecha_alta = models.DateField()
    fecha_baja = models.DateField()
    error = models.IntegerField(default=0) # Para marcar ante error de carga
