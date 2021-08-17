from typing import cast
from django.shortcuts import render
from .models import Libro, Autor, EjemplarEspecifico, Genero
from django.views import generic
# Create your views here.

def index(request):
    """
    Función vista para la página inicio del sitio. Esta es una función asociada a una un documento html o plantilla, en este caso al html principal. Luego veremos que el resto de vistas son clases heredadas, conocidas como vistas genéricas, que ya viene con todas las funcionalidades implementadas, con las pilas incluidas y sin necesidad de repetir tanto código (DRY), como dice django.
    """
    # Genera contadores de algunos de los objetos principales
    #num_libros = Libro.objects.all().count() #Recuerde que podemos usar el atributo-método count() directamente en cualquier expresión, en este caso, en el diccionario en el retorno de la función render. Por pedagogía usamos identificadores(variables) para intermediar.

    num_ejemEspe = EjemplarEspecifico.objects.count() #El atributo all() es prescindible.
    # Libros disponibles (status = 'd'):
    num_ejem_dispon = EjemplarEspecifico.objects.filter(status__exact='d').count()
    num_autores = Autor.objects.count()  # El 'all()' esta implícito por defecto.
    num_generos = Genero.objects.count()
    subTotal1 = num_autores + num_generos
    autoresPoe = Autor.objects.filter(apellido__iexact='Poe').count() # __exact refiere a la columna completa y la opera con el operador que se use. La i como prefijo hace que no distinga entre mayúsculas y minúsculas.
    cantTítulosCuervo = Libro.objects.filter(titulo__icontains = 'cuervo').count() # __contains refiere a una fracción de la la cadena contenida en la columna o campo de tipo string en la clase o modelo Libro. Ya sabemos que hace la i.
    #Debes tener en cuenta que cuando usas el metodo filter estas obteniendo una colección de objetos queryset y no una lista python, por eso sólo puede ser usado directamente si retorna un sólo objeto. Para obtener los elementos cuando retorna más de uno, extraer del queryset el atributo (columna de la tabla) a cada uno de los objetos en dicha colección (.objects.all), dónde all es prescindible.
    
    """
    lista=[]
    for elemento in Libro.objects.all().filter(titulo__icontains = 'cuervo'):
        lista.append(elemento.titulo)
    #Con este método en base a lista, se debe usar 'titConCuervo':str(lista)[1:-1] en el diccionario en la función render para convertir la lista en string y eliminar los corchetes. Esta forma es más larga.
    """
    títulosConCuervo = ""
    for elemento in Libro.objects.filter(titulo__icontains = 'cuervo'): #Vemos como el objects.all() sigue siendo prescindible. Al igual que .net, el uso de la s en objects como plural, hace explicito que se trata de una colección de uno o más objetos que son iterables para for-in.
        títulosConCuervo += "\"" + elemento.titulo + "\"" +", " # Usamos un acumulador para formar la lista de libros. Note el escape para poder colocar las comillas dobles a las cadenas elemento.tutulo. Recuerde que elemento.titulo es un string o cadena.
    # Con este método, se debe usar el rebanador 'titConCuervo':títulosConCuervo[0:-2] para rebanar (slicer) eliminar el espacio adelante, y la coma colgante y espacio al final de la cadena que se envia con el diccionario apuntada con el identificador context desde la función render que retorna esta vista index(). Ya habíamos visto funciones que retornan una función.

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(request, 'index.html', context={'num_libros':Libro.objects.all().count(),'num_ejemEspe':num_ejemEspe,'num_ejem_disponibles':num_ejem_dispon,'num_autores':num_autores, 'numero_generos':num_generos, 'totalGeneAutor1':subTotal1, 'conPoe':autoresPoe, 'numTítulosconCuervo':cantTítulosCuervo, 'titConCuervo':títulosConCuervo[0:-2]}, )

#Fijese la forma más sencilla de conformar una vista genérica, en este caso, una vista genérica de tipo list. Note también que es una clase, y no una función como index(request):
class VistaListaDeLibros(generic.ListView):
    model = Libro #De la clase-modelo Libro.
    paginate_by = 2 # Activamos la propiedad de paginación en la plantilla de esta vista generica (libro_list.html), creada en la plantilla base_generica.html. Hace que se véa en el documento html (plantilla) por lotes de dos en dos. En eso consiste la paginación de un documento.

#Como sabemos, las vistas genéricas no necesitan función renderizadora: se relacionan automáticamente con sus respectivas plantillas vinculadas, _list y _detail según el tipo de vista genérica de que se trate, y se encuentran en la carpeta con el nombre de la aplicación (catalogo) dentro de la carpeta templates.

#Y aquí una de tipo detalle (detail), respectivamente:
class VistaDetalleDeLibro(generic.DetailView):
    model = Libro  #Mismo modelo Libro, distinto tipo de vista genérica (generic.DetailView)

class VistaListaDeAutores(generic.ListView):
    model = Autor 

class VistaDetalleDeAutor(generic.DetailView):
    model = Autor #sigue siendo de la clase-modelo Autor, pero heredera de la clase generic.DetailView
