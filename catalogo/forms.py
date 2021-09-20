import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class FormRenovLibro(forms.Form):
    #Definimos el atributo-campo de tipo DateField, campoFechaDeRenovacion:
    campoFechaDeRenovacion = forms.DateField(help_text="Introduzca una fecha entre ahora y 4 semanas (predeterminado 3 semanas).", label="Ingrese fecha de renovación")

    def clean_campoFechaDeRenovacion(self): #Ojo: la palabra clean_ en el nombre de este método es reservada de django. El método clean_... se puede decir que es una especie de método "semi-builtin" de django, cuyo nombre debe tener la sintaxis clean_nombreDelCampoQueSeEvalúa. En este caso como estamos usando el campo atributo de esta clase, campoFechaDeRenovacion, de tipo forms.DateField, el nombre del atributo-método debe ser, clean_campoFechaDeRenovacion. Este es un método que lo ejecuta django automáticamente, cada vez que se evalúa el método is_valid() en la vista basada en función, RenovacionLibroPorLibrero de este ejemplo. En base al resultado de la ejecución de dicha vista, de ser válido el resultado, dirige o envía al usuario a la plantilla html referenciada con los datos pertinentes a reverse('VistaBibliotecarios1'). En caso de no ser válida (fecha para entrega anterior a la actual, o más allá de las 4 semanas), redirige nuevamente a la plantilla actual (libroRenovadoPorLibrero.html), con la impresión de los mensajes de error configurados para el caso, en los constructores ValidationError(), los cuales colocará encima del control-formulario, formu.as_table. Perdí un día en descubrir esto (por el método de tirar flechas o ensayo y error, por no saber bién la teoría).
        data = self.cleaned_data['campoFechaDeRenovacion'] #El atributo cleaned_data limpiará la entrada del campo, cambiando el formato del texto introducido por el usuario, en un sólo tipo predefinido por el usuario django(desarrollador), haciéndolo consistente. En este ejemplo se refiere al formato en que el usuario introduzca la fecha (dd-mm-aa, aa-mm-dd, dd/mm/aa, etc.), o desplegando un mensaje de error si se intenta ingresar texto diferenta a fechas como texto normal, caracteres no validos para enviar contenido malicioso al servidor, ataques con inyecciones sql, etc.

        # Chequea si la fecha de renovación introducida no está en el pasado.
        if data < datetime.date.today():
            raise ValidationError(_('Fecha inválida! - intenta renovar a una fecha pasada!'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Fecha inválida! - intenta renovar a una fecha más alla de las 4 semanas...'))

        # Remember to always return the cleaned data.
        return data