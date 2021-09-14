import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class FormRenovLibro(forms.Form):
    #Definimos el atributo-campo de tipo DateField, campoFechaDeRenovacion:
    campoFechaDeRenovacion = forms.DateField(help_text="Introduzca una fecha entre ahora y 4 semanas (predeterminado 3 semanas).")

    def clean_campoFechaDeRenovacion(self): #Ojo: la palabra clean_ en el nombre de este método es reservada de django: el método clean_... es un método built-in de django cuyo nombre debe tener la sintaxis clean_nombreDelCampoQueSeEvalúa. En este caso como estamos usando el campo atributo de esta clase, campoFechaDeRenovacion, de tipo forms.DateField, el nombre del atributo-método debe ser, clean_campoFechaDeRenovacion. Este es un método que lo ejecuta django automáticamente, cada vez que se evalúa el método is_valid() en la vista basada en función, RenovacionLibroPorLibrero de este ejemplo. En base al resultado de la ejecución de dicha vista, envía a la plantilla html referenciada con los datos pertinentes por reverse('VistaBibliotecarios1'), si es válida, o en caso de no serlo (fecha para entrega anterior a la actual, o más allá de las 4 semanas), redirige nuevamente a la plantilla actual (libroRenovadoPorLibrero.html), con la impresión de los mensajes configurados para el caso en los constructores ValidationError(), encima del control-formulario, formu.as_table. Perdí un día en descubrir esto (por el método de tirar flechas o ensayo y error, por no saber bién la teoría).
        data = self.cleaned_data['campoFechaDeRenovacion']

        # Chequea si la fecha de renovación introducida no está en el pasado.
        if data < datetime.date.today():
            raise ValidationError(_('Fecha inválida! - intenta renovar a una fecha pasada!'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Fecha inválida! - intenta renovar a una fecha más alla de las 4 semanas...'))

        # Remember to always return the cleaned data.
        return data