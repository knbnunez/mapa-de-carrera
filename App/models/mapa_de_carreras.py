from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Instituto(models.Model):
    nombre = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre
    

class Carrera(models.Model):
    nombre = models.CharField(max_length=255)
   
    def __str__(self):
        return self.nombre
    

class Carrera_Instituto(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    instituto = models.ForeignKey(Instituto, on_delete=models.CASCADE)
    

class Materia(models.Model):
    nombre = models.CharField(max_length=255)
   
    def __str__(self):
        return self.nombre


class Materia_Carrera(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)


class Docente(models.Model):
    legajo = models.IntegerField(primary_key=True) # legajo
    numero_documento = models.IntegerField(unique=True) # numero_documento
    nombre_apellido = models.CharField(max_length=255) # agente
    correo_electronico = models.EmailField(null=True, default=None) # correo_electronico

    def __str__(self):
        return self.nombre_apellido
       
 
# class Resolucion(models.Model):
#     nombre = models.CharField(max_length=255)
#     # De las dudas: las fechas son las mismas que podemos obtener del endpoint de /agentes/{legajo}/cargos ???
#     fecha_inicio = models.DateField()
#     fecha_fin = models.DateField()
#     documento = models.ImageField(upload_to='pdf')
    
#     def __str__(self):
#         return self.nombre
    

class Categoria(models.Model):
    codigo = models.CharField(primary_key=True, max_length=50) # categoria
    desc_categ = models.CharField(max_length=255) # desc_dedic
    
    def __str__(self):
        return self.desc_categ
    

class Modalidad(models.Model):
    desc_modal = models.CharField(max_length=255)
    
    def __str__(self):
        return self.desc_modal
    
    
class Dedicacion(models.Model):
    desc_dedic = models.CharField(max_length=255)
    
    def __str__(self):
        return self.desc_dedic
    

class Tipo_Extra(models.Model):
    desc_extra = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre     

    
class Ubicacion(models.Model):
    nombre = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre 


class Comision(models.Model):
    nombre = models.CharField(max_length=255)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
    
class Comision_Carrera(models.Model):
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
    
class Cargo(models.Model):
    nro_cargo = models.IntegerField(primary_key=True) # En la API de Mapuche lo usan como si fuera un nro de legajo, nosotros lo vamos a usar como nro_cargo, desde Mapuche se consume como: 'cargo'
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    
    # Propio o Guaraní?
    dependencia_desempeno = models.ForeignKey(Instituto, on_delete=models.CASCADE, related_name='cargo_desmpeno', null=True, default=None)
    dependencia_designacion = models.ForeignKey(Instituto, on_delete=models.CASCADE, related_name='cargo_designacion', null=True, default=None)
    
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, null=True)
    dedicacion = models.ForeignKey(Dedicacion, on_delete=models.CASCADE, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    fecha_alta = models.DateField()
    fecha_baja = models.DateField(null=True, blank=True)
    activo = models.IntegerField(        
        validators=[
            MinValueValidator(0, message='El valor debe ser 0 o 1.'),
            MaxValueValidator(1, message='El valor debe ser 0 o 1.')
        ]
    )

    resolucion = models.FileField(upload_to='media/', null=True, blank=True)


# Tanto para las comisiones como para las tareas extras (van a tener que inventar horas y fechas desde y hasta si no las tienen definidas)
class Carga_Horaria(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE, null=True, default=None) # Cuando sea tipo_extra: comision = null
    tipo_extra = models.ForeignKey(Tipo_Extra, on_delete=models.CASCADE, null=True, default=None) # Cuando sea comision: tipo_extra = null
    fecha_desde = models.CharField(max_length=100)
    fecha_hasta = models.CharField(max_length=100)
    hora_inicio = models.CharField(max_length=100)
    hora_finalizacion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
