# Generated by Django 4.1.7 on 2023-09-06 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0023_alter_tipo_extra_ch_cant_horas_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_Dictado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
    ]
