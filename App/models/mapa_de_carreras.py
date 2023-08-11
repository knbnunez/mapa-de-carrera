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


class Carga_Horaria(models.Model):
    hora_inicio = models.CharField(max_length=8)
    hora_fin = models.CharField(max_length=8)
    dia_semana = models.CharField(max_length=25)
    fecha_desde = models.CharField(max_length=10)
    fecha_hasta = models.CharField(max_length=10)


class Comision_CH(models.Model):
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE)
    carga_horaria = models.ForeignKey(Carga_Horaria, on_delete=models.CASCADE)


class Tipo_Extra_CH(models.Model):
    tipo_extra = models.ForeignKey(Tipo_Extra, on_delete=models.CASCADE)
    carga_horaria = models.ForeignKey(Carga_Horaria, on_delete=models.CASCADE)


# Debe ser llenado en asignar-comision u en el general de asignar-franja-horaria
class Cargo_CTE_CH(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    # uno siempre será null
    comision_ch = models.ForeignKey(Comision_CH, on_delete=models.CASCADE, null=True, default=None)
    tipo_extra_ch = models.ForeignKey(Tipo_Extra_CH, on_delete=models.CASCADE, null=True, default=None)