
#
#
#   Para ver cómo habíamos definido la restricción de horas,
#   ya no va a estar más en el modelo la restricción,
#   la comprobación estará en el momento de revisar si está excedido de horas
#
#

from django.db import models


class Modalidad(models.Model):
    desc_modal = models.CharField(max_length=255)
    
    def __str__(self):
        return self.desc_modal
    
    
class Dedicacion(models.Model):
    desc_dedic = models.CharField(max_length=255)
    
    def __str__(self):
        return self.desc_dedic



# TO DO: crear las instancias con las restricciones
class Modalidad_Dedicacion(models.Model):
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, null=True, default=None) # Se crea cuando se le asigna la modalidad al docente
    dedicacion = models.ForeignKey(Dedicacion, on_delete=models.CASCADE, null=True)
    restriccion_horas_minimas = models.IntegerField(null=True, default=None) # Se define implícitamente al crear una instancia
    restriccion_horas_maximas = models.IntegerField(null=True, default=None) # Ídem
    # error = models.IntegerField(default=0) # Para marcar ante error de carga

    # Restricciones:
    def save(self, *args, **kwargs):
        if self.modalidad is None: # Caso todavía no está definida la modalidad, no se aplica la restricción 
            super(Modalidad_Dedicacion, self).save(*args, **kwargs)
            return
        dedicacion = Dedicacion.objects.get(id=self.dedicacion.id) # Hay que asegurarse de que la dedicación asignada siempre exista, eso se controla en las views
        modalidad = Modalidad.objects.get(id=self.modalidad.id)
        # TO DO: definir restricciones
        if dedicacion.desc_dedic == 'Simple' and modalidad.desc_modal == 'Docencia/Desarrollo profesional':
            self.restriccion_horas_minimas = 4
            self.restriccion_horas_maximas = 6
        elif dedicacion.desc_dedic == 'Semided.' and modalidad.desc_modal == 'Docencia/Desarrollo profesional':
            self.restriccion_horas_minimas = 6
            self.restriccion_horas_maximas = 10
        elif dedicacion.desc_dedic == 'Semided.' and modalidad.desc_modal == 'Docencia e Investigación':
            self.restriccion_horas_minimas = 4
            self.restriccion_horas_maximas = 6
        elif dedicacion.desc_dedic == 'Exclusiva' and modalidad.desc_modal == 'Docencia e Investigación':
            self.restriccion_horas_minimas = 4
            self.restriccion_horas_maximas = 8
        
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