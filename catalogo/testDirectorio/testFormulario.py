import datetime

from django.test import TestCase
from django.utils import timezone

from catalogo.forms import FormRenovLibro

class ClasePruebaFormRenov(TestCase):
    def testEtiquetaFormRenov(self):
        formulario = FormRenovLibro()
        self.assertTrue(formulario.fields['campoFechaDeRenovacion'].label is None or formulario.fields['campoFechaDeRenovacion'].label == 'Ingrese fecha de renovación')

    def testEtiquetaFormRenov_help_text(self):
        formu = RenewBookForm()
        self.assertEqual(formu.fields['campoFechaDeRenovacion'].help_text, 'Introduzca una fecha entre ahora y 4 semanas (predeterminado 3 semanas).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    