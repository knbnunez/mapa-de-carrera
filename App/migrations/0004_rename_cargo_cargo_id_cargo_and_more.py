# Generated by Django 4.1.7 on 2023-03-02 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_rename_id_cargas_extras_cargo_id_cargo_carga_extra_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cargo',
            old_name='cargo',
            new_name='id_cargo',
        ),
        migrations.RenameField(
            model_name='cargo',
            old_name='categoria',
            new_name='id_categoria',
        ),
        migrations.RenameField(
            model_name='categoria',
            old_name='categoria',
            new_name='id_categoria',
        ),
    ]