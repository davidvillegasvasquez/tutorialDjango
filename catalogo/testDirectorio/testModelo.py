from django.test import TestCase

from catalogo.models import Autor, Genero

class PruebaModeloAutor(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Autor.objects.create(nombre='David', apellido='Villegas')

    def testEtiquetaNombre(self):
        autor = Autor.objects.get(id=1)
        compoEtiqueta = autor._meta.get_field('nombre').verbose_name
        self.assertEqual(compoEtiqueta, 'nombre')

    def testEtiquetaFechaMuerte(self):
        autor = Autor.objects.get(id=1)
        campoEtiqueta = autor._meta.get_field('fecha_muerte').verbose_name
        self.assertEqual(campoEtiqueta, 'Muerte')

    def testNombreLongitudMax(self):
        autor = Autor.objects.get(id=1)
        longitudMax = autor._meta.get_field('nombre').max_length
        self.assertEqual(longitudMax, 100)

    def test_nombreDelObjeto_es_nombre_coma_apellido(self):
        autor = Autor.objects.get(id=1)
        excepcion_objeto_nombre = f'{autor.nombre}, {autor.apellido}'
        self.assertEqual(str(autor), excepcion_objeto_nombre)

    def testObtenerUrlAbsoluta(self):
        autor = Autor.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(autor.get_absolute_url(), '/catalogo/autor/1')

class PruebaModeloGenero(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Genero.objects.create(nombre='Checo')

    def testEtiquetaNombre(self):
        genero = Genero.objects.get(id=1)
        campoEtiqueta = genero._meta.get_field('nombre').verbose_name
        self.assertEqual(campoEtiqueta, 'nombre')

    def testNombreLongitudMax(self):
        genero = Genero.objects.get(id=1)
        longitudMax = genero._meta.get_field('nombre').max_length
        self.assertEqual(longitudMax, 200)
