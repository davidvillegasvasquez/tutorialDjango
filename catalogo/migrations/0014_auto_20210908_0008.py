# Generated by Django 3.1.4 on 2021-09-08 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0013_auto_20210907_2047'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ejemplarespecifico',
            options={'ordering': ['devolucion'], 'permissions': (('permisoBibliotecario1', 'Permiso tipo 1 sólo para bibliotecarios'), ('unPermisoX', 'Un permiso de hacer x cosa a x usuario.'))},
        ),
    ]
