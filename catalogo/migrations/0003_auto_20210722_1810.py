# Generated by Django 3.1.4 on 2021-07-22 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0002_auto_20210722_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lenguaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)", max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='libro',
            name='lenguaje',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogo.lenguaje'),
        ),
    ]
