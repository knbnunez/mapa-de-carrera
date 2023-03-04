from django.db import models


class Instituto(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    instituto = models.ForeignKey(Instituto, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.nombre
    
    
class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    carrera = models.ManyToManyField(Carrera)
   
    def __str__(self):
        return self.nombre


class Docente(models.Model):
    legajo = models.IntegerField(primary_key=True) # legajo
    numero_documento = models.IntegerField(unique=True) # numero_documento
    nombre_apellido = models.CharField(max_length=255) # agente
    correo_electronico = models.EmailField(null=True, default=None) # correo_electronico

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
    categoria = models.CharField(primary_key=True, max_length=50) # categoria
    desc_categ = models.CharField(max_length=100) # desc_dedic
    
    def __str__(self):
        return self.nombre
    

class Modalidad(models.Model):
    desc_modal = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    
class Dedicacion(models.Model):
    desc_dedic = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    
# TO DO: crear las instancias con las restricciones
class Modalidad_Dedicacion(models.Model):
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, null=True, default=None) # Se crea cuando se le asigna la modalidad al docente
    dedicacion = models.ForeignKey(Dedicacion, on_delete=models.CASCADE, null=True)
    restriccion_horas_minimas = models.IntegerField(null=True, default=None) # Se define implícitamente al crear una instancia
    restriccion_horas_maximas = models.IntegerField(null=True, default=None) # Ídem
    error = models.IntegerField(default=0) # Para marcar ante error de carga

    # Restricciones:
    def save(self, *args, **kwargs):
        if self.modalidad is None: # Caso todavía no está definida la modalidad, no se aplica la restricción 
            super(Modalidad_Dedicacion, self).save(*args, **kwargs)
        dedicacion = Dedicacion.objects.get(id=self.dedicacion.id) # Hay que asegurarse de que la dedicación asignada siempre exista, eso se controla en las views
        modalidad = Modalidad.objects.get(id=self.modalidad.id)
        # TO DO: definir restricciones
        if dedicacion.desc_dedic == 'Simple' and modalidad.desc_modal == 'Docencia/Desarrollo profesional':
            self.restriccion_horas_minimas = 0
            self.restriccion_horas_maximas = 0
        elif dedicacion.desc_dedic == 'Semided.' and modalidad.desc_modal == 'Docencia/Desarrollo profesional':
            self.restriccion_horas_minimas = 0
            self.restriccion_horas_maximas = 0
        elif dedicacion.desc_dedic == 'Semided.' and modalidad.desc_modal == 'Docencia e Investigación':
            self.restriccion_horas_minimas = 0
            self.restriccion_horas_maximas = 0
        elif dedicacion.desc_dedic == 'Exclusiva' and modalidad.desc_modal == 'Docencia e Investigación':
            self.restriccion_horas_minimas = 0
            self.restriccion_horas_maximas = 0
        
        # Para la restricción de la restricción de las combinaciones de arriba, definirlas en el template, si la dedicación es 'Simple', sólo mostrar 'Docencia/Desarrollo profesional' en el drop down list.
        
        super(Modalidad_Dedicacion, self).save(*args, **kwargs)

        # Modalidad Docencia/Desarrollo profesional:
        # - Dedicación Semiexclusiva:
        #       - Frente al aula: 10 hrs (máx) y 6 hrs (mín)
        # - Dedicación Simple:
        #       - Frente al aula: 6 hrs (máx) y 4 hrs (mín)

        # Modalidad Docencia e Investigación:
        # - Dedicación Exclusiva:
        #       - Frente al aula: 8 hrs (máx) y 4 hrs (mín)
        # - Dedicación Semiexclusiva:
        #       - Frente al aula: 6 hrs (máx) y 4 hrs (mín)

    
    
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
    materia = models.ManyToManyField(Materia)
    periodo_electivo = models.ForeignKey(Periodo_Electivo, on_delete=models.CASCADE)
    franja_horaria = models.ManyToManyField(Franja_Horaria)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
    
class Cargo(models.Model):
    # Mapuche
    nro_cargo = models.IntegerField(primary_key=True) # En la API de Mapuche lo usan como si fuera un nro de legajo
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    # Propio
    resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE, null=True, default=None)
    # Propio o Guaraní?
    dependencia_desempeno = models.ForeignKey(Instituto, on_delete=models.CASCADE, related_name='cargo_desmpeno', null=True, default=None)
    dependencia_designacion = models.ForeignKey(Instituto, on_delete=models.CASCADE, related_name='cargo_designacion', null=True, default=None)
    # Propio - Mapuche
    modalidad_dedicacion = models.ForeignKey(Modalidad_Dedicacion, on_delete=models.CASCADE, null=True)
    # Propio
    carga_extra = models.ManyToManyField(Cargas_Extras, default=None) # null=True
    franja_horaria = models.ManyToManyField(Franja_Horaria, default=None)
    # Mapuche
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    fecha_alta = models.DateField()
    fecha_baja = models.DateField()
