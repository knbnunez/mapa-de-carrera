# Generated by Django 4.1.7 on 2023-03-02 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_alter_docente_correo_electronico'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cargo',
            old_name='id_cargas_extras',
            new_name='id_cargo_carga_extra',
        ),
        migrations.RenameField(
            model_name='cargo',
            old_name='id_franja_horaria',
            new_name='id_cargo_franja_horaria',
        ),
    ]