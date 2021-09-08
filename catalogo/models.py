from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Genero(models.Model):
    """
    Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.).
    """
    nombre = models.CharField(max_length=200, help_text="Ingrese el tipo de género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return self.nombre

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Libro(models.Model):
    """
    Modelo que representa un libro (pero no un Ejemplar específico).
    """

    titulo = models.CharField(max_length=200)

    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Autor' es un string no un objeto.
    resumen = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")
    isbn = models.CharField('ISBN',max_length=13, help_text='hasta 13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genero = models.ManyToManyField(Genero, help_text="seleccione un genero para este libro.")
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.

    lenguaje = models.ForeignKey('Lenguaje', on_delete=models.SET_NULL, null=True)

    def display_genero(self):
        """
        Creates a string for the Genero. This is required to display genre in Admin."""
        return ', '.join([ genero.nombre for genero in self.genero.all()[:3] ])     
    display_genero.short_description = 'Genero'

    def __str__(self):
        """
        String que representa al objeto Libro
        """
        return self.titulo

    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Libro
        """
        return reverse('libro-detail', args=[str(self.id)])

import uuid # Requerida para las instancias de libros únicos.

class EjemplarEspecifico(models.Model):
    """
    Modelo que representa una copia específica de un libro (Una copia que puede ser prestada por la biblioteca). Como cada clae es un modelo, que a su vez representa una tabla en al base de datos, por lo tanto puede tener muchos atributos-campos tipo objetos models.ForeingKey, pero sólo uno tipo primary_key, bajo la formo de objeto models.UUIDField. Note que el identificador-apuntador hacia este objeto se torna al color tipo clase o función.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True)
    impresion = models.CharField(max_length=200)
    devolucion = models.DateField(null=True, blank=True)
    prestatario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) #Note que el argumento de primero en la instanciación del objeto/clase, models.ForeingKey, User, representa una tabla o clase implicita de django, consistente en todos los usuarios de la aplicación django, guardados en la base de datos.
    campoConstante = 'xxx' #Podemos meter un atributo-campo como una constante simbólica. Todos los registros o filas tendrán este valor en su campo o columna.
    PRESTAMO_STATUS = (
        ('m', 'Mantenimiento'),
        ('p', 'Prestado'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
    )

    status = models.CharField(max_length=1, choices=PRESTAMO_STATUS, blank=True, default='m', help_text='Estatus en que se encuentra actualmente el ejemplar específico.')

    class Meta:
        ordering = ["devolucion"]
        permissions = (("permisoBibliotecario1", "Permiso tipo 1 sólo para bibliotecarios"), ("permisoBibliotecario2", "Permiso tipo 2 sólo para bibliotecarios"), ("unPermisoX", "Un permiso de hacer x cosa a x usuario."), )

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.id, self.libro.titulo)

    #@property  #No se para que sirve este decorador, de hecho está comentado y no pasó nada.
    def esta_atrasado(self): #Método-atributo para determinar si está atrasado en la devolución.
        if self.devolucion and date.today() > self.devolucion:
            return True
        return False

class Autor(models.Model):
    """
    Modelo que representa un autor
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    fecha_muerte = models.DateField('Muerte', null=True, blank=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('autor-detail', args=[str(self.id)])

    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s, %s' % (self.nombre, self.apellido)

class Lenguaje(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    nombre = models.CharField(max_length=200,
                            help_text="Introduzca el idioma del libro.")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.nombre


