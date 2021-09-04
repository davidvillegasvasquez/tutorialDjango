from typing import cast
from django.shortcuts import render
from .models import Libro, Autor, EjemplarEspecifico, Genero
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
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

#VistaListaDeLibrosPrestadosPorUsuario = LoanedBooksByUserListView
class VistaDeLosUsuarios(LoginRequiredMixin, generic.ListView):
    """Clase generica basada en vista tipo lista, para los libros prestados al usuario actual."""
    #permission_required = 'catalogo.permiso_usuario' #No requiere ningún permiso.
    model = EjemplarEspecifico
    template_name ='catalogo/vistausuarios.html' #El nombre de la plantilla aquí es arbitrario por el usuario.
    paginate_by = 10

    def get_queryset(self):
        return EjemplarEspecifico.objects.filter(prestatario=self.request.user).filter(status__exact='p').order_by('devolucion')

class VistaDeLosBibliotecarios(PermissionRequiredMixin, generic.ListView):
    """Clase generica basada en vista tipo lista, para los libros prestados al usuario actual."""
    
    model = EjemplarEspecifico
    permission_required = 'catalogo.can_mark_retornado' #Vista sólo ejecutable para usuarios.
    template_name ='catalogo/vistabibliotecarios.html' #El nombre de la plantilla aquí es arbitrario por el usuario.
    paginate_by = 10

    def get_queryset(self):
        return EjemplarEspecifico.objects.filter(status__exact='p').order_by('devolucion')