# Generated by Django 4.2.5 on 2023-11-11 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0003_remove_asignatura_id_tipoasignatura_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jefe_carrera',
            name='id_usuario',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
