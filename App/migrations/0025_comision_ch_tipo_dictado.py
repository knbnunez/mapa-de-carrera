# Generated by Django 4.1.7 on 2023-09-06 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0024_tipo_dictado'),
    ]

    operations = [
        migrations.AddField(
            model_name='comision_ch',
            name='tipo_dictado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='App.tipo_dictado'),
        ),
    ]
