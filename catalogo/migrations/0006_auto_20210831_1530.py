# Generated by Django 3.1.4 on 2021-08-31 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogo', '0005_auto_20210723_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ejemplarespecifico',
            options={'ordering': ['devolucion'], 'permissions': (('puede_marcar_retornado', 'Poner como devuelto'),)},
        ),
        migrations.AddField(
            model_name='ejemplarespecifico',
            name='prestados',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
