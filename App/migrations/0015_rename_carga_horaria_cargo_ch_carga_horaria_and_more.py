# Generated by Django 4.1.7 on 2023-08-09 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0014_rename_carga_horaria_cargo_ch_carga_horaria_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cargo_ch',
            old_name='carga_Horaria',
            new_name='carga_horaria',
        ),
        migrations.RenameField(
            model_name='comision_ch',
            old_name='carga_Horaria',
            new_name='carga_horaria',
        ),
        migrations.RenameField(
            model_name='tipo_extra_ch',
            old_name='carga_Horaria',
            new_name='carga_horaria',
        ),
    ]