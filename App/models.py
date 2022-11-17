from django.db import models

# Create your models here.

# Acá haces el modelo vos

class MODELNAME(models.Model):
    """Model definition for MODELNAME."""

    

    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'MODELNAME'
        verbose_name_plural = 'MODELNAMEs'

    def __str__(self):
        """Unicode representation of MODELNAME."""
        pass
