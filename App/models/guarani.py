from django.db import models


class SgaUbicaciones(models.Model):
    ubicacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'sga_ubicaciones'


class SgaResponsablesAcademicas(models.Model):
    responsable_academica = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'sga_responsables_academicas'
        # unique_together = (('institucion', 'codigo'),)


class SgaPropuestas(models.Model):
    propuesta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sga_propuestas'


class SgaPropuestasRa(models.Model):
    propuesta = models.ForeignKey('SgaPropuestas', models.DO_NOTHING, db_column='propuesta')
    responsable_academica = models.ForeignKey('SgaResponsablesAcademicas', models.DO_NOTHING, db_column='responsable_academica')

    class Meta:
        managed = False
        db_table = 'sga_propuestas_ra'
        # unique_together = (('propuesta', 'responsable_academica'),)


class SgaElementos(models.Model):
    elemento = models.AutoField(primary_key=True) # No cambiar el nombre del atributo, sirve para cursor pueda hacer la consulta a la BD
    nombre = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sga_elementos'


class SgaComisiones(models.Model):
    comision = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    elemento = models.ForeignKey(SgaElementos, models.DO_NOTHING, db_column='elemento')
    ubicacion = models.ForeignKey(SgaUbicaciones, models.DO_NOTHING, db_column='ubicacion')
    
    class Meta:
        managed = False
        db_table = 'sga_comisiones'
        # unique_together = (('elemento', 'periodo_lectivo', 'ubicacion', 'nombre'),)


class SgaAsignaciones(models.Model):
    asignacion = models.AutoField(primary_key=True)
    dia_semana = models.CharField(max_length=10, blank=True, null=True)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_finalizacion = models.TimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'sga_asignaciones'


class SgaComisionesBH(models.Model):
    banda_horaria = models.AutoField(primary_key=True)
    comision = models.ForeignKey(SgaComisiones, models.DO_NOTHING, db_column='comision')
    asignacion = models.ForeignKey(SgaAsignaciones, models.DO_NOTHING, db_column='asignacion')
    
    class Meta:
        managed = False
        db_table = 'sga_comisiones_bh'
        # unique_together = (('comision', 'asignacion'),)


class SgaComisionesPropuestas(models.Model):
    comision = models.ForeignKey(SgaComisiones, models.DO_NOTHING, db_column='comision', primary_key=True)
    propuesta = models.ForeignKey(SgaPropuestas, models.DO_NOTHING, db_column='propuesta')

    class Meta:
        managed = False
        db_table = 'sga_comisiones_propuestas'
        # unique_together = (('comision', 'propuesta', 'plan'),)


# Elminar: es solo para cargar datos de prueba
class sgaDocentes(models.Model):
    docente = models.AutoField(primary_key=True)
    legajo = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'sga_docentes'


# Eliminar
class sgaDocentesComision(models.Model):
    docente = models.ForeignKey(sgaDocentes, models.DO_NOTHING, db_column='docente')
    comision = models.ForeignKey(SgaComisiones, models.DO_NOTHING, db_column='comision')
    class Meta:
        managed = False
        db_table = 'sga_docentes_comision'
    
    