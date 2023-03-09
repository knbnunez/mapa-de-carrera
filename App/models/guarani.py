from django.db import models


# Agregar todas las tablas que nos interese usar de la BD de Guaraní
class sga_elementos(models.Model): # Materias
    elemento = models.CharField(primary_key=True)
    nombre = models.CharField()
    codigo = models.CharField()

    class Meta:
        managed = False # Es necesario para que Django no cree las tablas en nuestra base de datos
        db_table = 'sga_comisiones_bh'
        # app_label = 'nombre_app_externa'
        using = 'guarani' # DB


class sga_comisiones(models.Model):
    comision = models.CharField(primary_key=True)
    nombre = models.CharField()
    elemento = models.ForeignKey(sga_elementos) # materia

    class Meta:
        managed = False
        db_table = 'sga_comisiones_bh'
        # app_label = 'nombre_app_externa'
        using = 'guarani' # DB


class sga_ubicaciones(models.Model):
    ubicacion = models.CharField(primary_key=True)
    nombre = models.CharField()

    class Meta:
            managed = False
            db_table = 'sga_comisiones_bh'
            # app_label = 'nombre_app_externa'
            using = 'guarani' # DB


class sga_asignaciones(models.Model):
    asignacion = models.CharField(primary_key=True)
    dia_semana = models.CharField()
    fecha_desde = models.CharField()
    fecha_hasta = models.CharField()
    hora_inicio = models.CharField()
    hora_fin = models.CharField()

    class Meta:
        managed = False 
        db_table = 'sga_comisiones_bh'
        # app_label = 'nombre_app_externa'
        using = 'guarani' # DB


class sga_comisiones_bh(models.Model):
    comision = models.ForeignKey(sga_comisiones)
    asignacion = models.ForeignKey(sga_asignaciones)
    elmento = models.ForeignKey()

    class Meta:
        managed = False
        db_table = 'sga_comisiones_bh'
        # app_label = 'nombre_app_externa'
        using = 'guarani' # DB

    # Luego para manejarlo desde el ORM: usuarios_externos = UsuarioExterno.objects.using('db_externa').all()