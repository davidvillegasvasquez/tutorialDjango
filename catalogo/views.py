from typing import cast
from django.shortcuts import render
from .models import Libro, Autor, EjemplarEspecifico, Genero
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from catalogo.forms import FormRenovLibro

# Create your views here.

def index(request):
    """
    Función vista para la página inicio del sitio. Esta es una función asociada a un documento html o plantilla, en este caso al html principal index.html. Luego veremos que el resto de vistas son clases heredadas, conocidas como vistas genéricas, que ya viene con todas las funcionalidades implementadas, con "las pilas incluidas", sin necesidad de repetir tanto código: DRY, como dice django.
    """
    # Genera contadores de algunos de los objetos principales
    #num_libros = Libro.objects.all().count() #Recuerde que podemos usar el atributo-método count() directamente en cualquier expresión, en este caso, en el diccionario en el retorno de la función render. Por pedagogía usamos identificadores(nombre de variables) para intermediar.

    num_ejemEspe = EjemplarEspecifico.objects.count() #El atributo all() es prescindible.
    # Libros disponibles (status = 'd'):
    num_ejem_dispon = EjemplarEspecifico.objects.filter(status__exact='d').count()
    num_autores = Autor.objects.count()  # El 'all()' esta implícito por defecto.
    num_generos = Genero.objects.count()
    subTotal1 = num_autores + num_generos
    autoresPoe = Autor.objects.filter(apellido__iexact='Poe').count() # __exact refiere a la columna completa, y la opera con el operador que se use. La i como prefijo hace que no distinga entre mayúsculas y minúsculas.
    cantTítulosCuervo = Libro.objects.filter(titulo__icontains = 'cuervo').count() # __contains refiere a una fracción de la cadena contenida en la columna o campo de tipo string en la clase o modelo Libro. Ya sabemos que hace la i.
    #Debes tener en cuenta que cuando usas el método filter, estas obteniendo una colección de objetos queryset, y no una lista python.

    #Hacemos el contador de visitas en base al atributo-valor num_visits del objeto request.session que se ejecutará cada vez que se invoque esta función o vista:
    acum_visitas = request.session.get('num_visits', 0)
    request.session['num_visits'] = acum_visitas + 1
    #request.session['num_visits'] = 0  #Con esta proposición reseteo el contador de visitas.
    títulosConCuervo = ""
    for elemento in Libro.objects.filter(titulo__icontains = 'cuervo'): #Vemos como el all() en objects sigue siendo prescindible. Al igual que .net, el uso de la s en objects como plural, hace explicito que se trata de una colección de uno o más objetos que son iterables para un ciclo for.
        títulosConCuervo += "\"" + elemento.titulo + "\"" +", " # Usamos un acumulador para formar la lista de libros. Note el escape para poder colocar las comillas dobles a las cadenas elemento.tutulo. Recuerde que elemento.titulo es un string o cadena referente al campo o columna titulo de la tabla-clase-modelo Libro.
    # Con este método, se debe usar el rebanador 'titConCuervo':títulosConCuervo[0:-2] para rebanar (slicer) eliminar el espacio adelante, y la coma colgante al final de la cadena que se envia con el diccionario, apuntada con el identificador context, desde la función render que retorna esta vista index(). Ya habíamos visto funciones que retornan una función.

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(request, 'index.html', context={'num_libros':Libro.objects.all().count(), 'num_ejemEspe':num_ejemEspe, 'num_ejem_disponibles':num_ejem_dispon, 'num_autores':num_autores, 'numero_generos':num_generos, 'totalGeneAutor1':subTotal1, 'conPoe':autoresPoe, 'numTítulosconCuervo':cantTítulosCuervo, 'titConCuervo':títulosConCuervo[0:-2], 'visitas':acum_visitas,})

#Fijese la forma más sencilla de conformar una vista genérica, en este caso, una vista genérica de tipo list. Note también que es una clase, y no una función como index(request):
class VistaListaDeLibros(generic.ListView):
    model = Libro #De la clase-modelo-tabla Libro.
    paginate_by = 2 # Activamos la propiedad de paginación en la plantilla de esta vista genérica (libro_list.html), propiedad creada en la plantilla madre, base_generica.html. Hace que se vea en el documento html (plantilla) por lotes de dos en dos los títulos de los libros que hay en la biblioteca. En eso consiste la paginación de un documento.

#Como sabemos, las vistas genéricas no necesitan función renderizadora: se relacionan automáticamente con sus respectivas plantillas vinculadas, _list y _detail, y se encuentran en la carpeta con el nombre de la aplicación (catalogo) dentro de la carpeta templates.

#Y aquí una de tipo detalle (detail), respectivamente:
class VistaDetalleDeLibro(generic.DetailView):
    model = Libro  #Mismo modelo Libro, distinto tipo de vista genérica (generic.DetailView)

#Con las características heredadas de LoginRequiredMixin (sólo para vistas basadas en clases), restringimos el acceso a esta vista según esté abierta una sesión o no:
#class VistaListaDeAutores(LoginRequiredMixin ,generic.ListView):
class VistaListaDeAutores(generic.ListView):
    model = Autor    

class VistaDetalleDeAutor(generic.DetailView):
    model = Autor #sigue siendo de la clase-modelo Autor, pero heredera de la clase generic.DetailView


class VistaEjemplaresParaLosUsuarios(LoginRequiredMixin, generic.ListView):
    """Clase generica basada en vista tipo lista, para los libros prestados al usuario actual. Su plantilla es vistausuarios.html"""
    #permission_required = 'catalogo.permiso_usuario' #No requiere ningún permiso.
    model = EjemplarEspecifico
    template_name ='catalogo/vista_usuarios.html' #El nombre de la plantilla aquí es arbitrario por el usuario.
    paginate_by = 10

    def get_queryset(self):#Se define lo 
        return EjemplarEspecifico.objects.filter(prestatario=self.request.user).filter(status__exact='p').order_by('devolucion')

class VistaEjemplaresParaBibliotecarios1(PermissionRequiredMixin, generic.ListView):
    """Clase generica basada en vista tipo lista, para los bibliotecarios"""
    
    model = EjemplarEspecifico
    permission_required = 'catalogo.permisoBibliotecario1' #Vista sólo bibliotecarios con permiso nivel 1 para estos (mostrará la plantilla referenciada abajo).
    template_name ='catalogo/vista_bibliotecarios1.html' #El nombre de la plantilla aquí es arbitrario por el usuario.
    paginate_by = 10

    def get_queryset(self):
        return EjemplarEspecifico.objects.filter(status__exact='p').order_by('devolucion')

class VistaEjemplaresParaBibliotecarios2(PermissionRequiredMixin, generic.ListView):
    """Una clase especial para este caso."""
    
    model = EjemplarEspecifico
    permission_required = 'catalogo.permisoBibliotecario2' 
    template_name ='catalogo/vista_bibliotecarios2.html' #El nombre de la plantilla aquí es arbitrario por el usuario.
"""
    paginate_by = 10

    def get_queryset(self):
        return EjemplarEspecifico.objects.filter(status__exact='p').order_by('devolucion')
"""

@login_required
@permission_required('catalogo.permisoBibliotecario1', raise_exception=True)
#Primera vista basada en función que se presenta en este ejemplo. Es por eso que para este tipo de vista, su referencia en el mapeador que la localiza no lleva la extensión .as_view() al final. No es una subclase.
def RenovacionLibroPorLibrero(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    libro_ejemEspecif = get_object_or_404(EjemplarEspecifico, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        formulario = FormRenovLibro(request.POST)

        # Check if the form is valid:
        if formulario.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field). El método is_valid() ejecuta implicitamente el método clean_campoFechaDeRenovacion de la clase FormRenovLibro a la que pertenece el objeto formulario.
            libro_ejemEspecif.devolucion = formulario.cleaned_data['campoFechaDeRenovacion'] #Recuerde que campoFechaDeRenovacion, es el campo de tipo fecha (DateField) de la clase de tipo form, FormRenovLibro, que está en el módulo forms.py.
            libro_ejemEspecif.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('VistaBibliotecarios1'))

    # If this is a GET (or any other method) create the default form. Y este formulario tendrá el mensaje de error en forma de lista ul por defecto, que se específico en la definición de su clase FormRenovLibro en forms.py
    else:
        fecha_propuesta_renov = datetime.date.today() + datetime.timedelta(weeks=3)
        formulario = FormRenovLibro(initial={'campoFechaDeRenovacion': fecha_propuesta_renov})

    context = {
        'formu': formulario,
        'libro_instancia': libro_ejemEspecif,
    }

    return render(request, 'catalogo/libroRenovadoPorLibrero.html', context)


