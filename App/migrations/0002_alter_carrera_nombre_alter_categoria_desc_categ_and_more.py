# Generated by Django 4.1.7 on 2023-03-11 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrera',
            name='nombre',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='desc_categ',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='comision',
            name='nombre',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='dedicacion',
            name='desc_dedic',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='instituto',
            name='nombre',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='localidad',
            name='nombre',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='materia',
            name='nombre',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='modalidad',
            name='desc_modal',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='resolucion',
            name='nombre',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='tipo_extra',
            name='desc_extra',
            field=models.CharField(max_length=255),
        ),
    ]
