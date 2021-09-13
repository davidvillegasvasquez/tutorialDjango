import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class FormRenovLibro(forms.Form):
    fecha_renovacion = forms.DateField(help_text="Introduzca una fecha entre ahora y 4 semanas (predeterminado 3 semanas).")

    def clean_fecha_renovacion(self): #Ojo: la palabra clean_ en el nombre de este método es reservada de django: este es un método buil-in de django cuyo nombre debe ser clean_nombreDelCampoQueSeEvalúa. En este caso como estamos usando el campo 'fecha_renovacion' de tipo forms.DateField de esta clase, el nombre del atributo-método debe ser clean_fecha_renovacion. Perdí un día en descubrir esto (por el método de tirar flechas o ensayo y error, por no saber bién la teoría).
        data = self.cleaned_data['fecha_renovacion']

        # Chequea si la fecha de renovación introducida no está en el pasado.
        if data < datetime.date.today():
            raise ValidationError(_('Fecha invalida - renovación en el pasado!'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Fecha invalida - renovación más alla de las 4 semanas'))

        # Remember to always return the cleaned data.
        return data