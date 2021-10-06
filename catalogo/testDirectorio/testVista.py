from django.test import TestCase

# Create your tests here.

class ClaseDePruebaCualquiera(TestCase):
    @classmethod

 #El método setUpTestData(cls) es para ejecutar una sóla vez para todos los métodos de la clase, para configurar datos no modificados. Su nombre es reservado por django, el usuario no lo puede definir con otro:
    def setUpTestData(cls):
        print("Método setUpTestData(cls) de testVista.py, y se ejecutará una sóla vez.")
        pass

#El método setUp(self) es para ejecutar uno por cada método de prueba en la clase para configurar datos limpios. Su nombre es reservado por django, el usuario no lo puede definir con otro:
    def setUp(self):
        print("Método setUp(self) de testVista.py(se ejecuta una vez para cada método):")
        pass

#Todos los métodos de prueba, así como el nombre del módulo de la clase propietaria de dichos métodos, y el directorio dónde están dichos módulos, deben comenzar con la palabra reservada test (test*) como prefijo para que django los pueda detectar como pruebas. Ej: testDirectorio, testModuloX.py, testMetodoDePrueba(self). El único que no necesita el prefijo test, es el nombre de la clase.
    def testDeFalsoEsFalso(self):
        print("- Método pruebaDeFalsoEsFalso(self).")
        self.assertFalse(1>3)

    def testDeFalsoEsVerdadero(self):
        print("- Método pruebaDeFalsoEsVerdadero(self).")
        self.assertTrue(True)

    def testUnoMasUnoEsDos(self):
        print("- Método pruebaUnoMasUnoEsDos(self).")
        self.assertEqual(1 + 1, 2)
