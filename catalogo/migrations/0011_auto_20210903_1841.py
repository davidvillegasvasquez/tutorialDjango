# Generated by Django 3.1.4 on 2021-09-03 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0010_auto_20210903_1620'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ejemplarespecifico',
            options={'ordering': ['devolucion'], 'permissions': (('can_mark_retornado', 'Coloca el libro como retornado'),)},
        ),
    ]
