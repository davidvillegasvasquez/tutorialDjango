from typing import cast
from django.shortcuts import render
from .models import Libro, Autor, EjemplarEspecifico, Genero
from django.views import generic
# Create your views here.

def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    #num_libros = Libro.objects.all().count() #Recuerde que podemos usar el atributo-método count() directamente en cualquier expresión, en este caso, en el diccionario.
    #Los otros atributos métodos igualmente se pueden poner directamente en el diccionario del tercer argumento de la función render, pero por fines didacticos los apuntamos con identificadores que serán los que serán usados en dicho diccionario.
    num_ejemEspe = EjemplarEspecifico.objects.count() #El atributo all() es prescindible.
    # Libros disponibles (status = 'd'):
    num_ejem_dispon = EjemplarEspecifico.objects.filter(status__exact='d').count()
    num_autores = Autor.objects.count()  # El 'all()' esta implícito por defecto.
    num_generos = Genero.objects.count()
    subTotal1 = num_autores + num_generos
    autoresPoe = Autor.objects.filter(apellido__iexact='Poe').count() # __exact refiere a la columna completa y la opera con el operador que se use. La i como prefijo hace que no distinga entre mayúsculas y minúsculas.
    cantTítulosCuervo = Libro.objects.filter(titulo__icontains = 'cuervo').count() # __contains refiere a una fracción de la la cadena contenida en la columna tipo string. Ya sabemos que hace la i.
    #Debes tener en cuenta que cuando usas el metodo filter estas obteniendo un queryset y no una lista python, por eso sólo puede ser usado directamente si retornar un sólo objeto. Para obtener los elementos cuando retorna más de uno, debes evaluar el queryset ya sea usando un slice, el metodo all de django o convirtiendo en lista con el cast list().
    #A continuación se debe extraer la columna o campo que se desea de cada uno de los objeto-instancia en el grupo de objetos objects u objects.all(), con una iteración for:
    """
    lista=[]
    for elemento in Libro.objects.all().filter(titulo__icontains = 'cuervo'):
        lista.append(elemento.titulo)
    #Con este método en base a lista, se debe usar 'titConCuervo':str(lista)[1:-1] en el diccionario en la función render para convertir la lista en string y eliminar los corchetes. Esta forma es más larga.
    """
    títulosConCuervo = ""
    for elemento in Libro.objects.filter(titulo__icontains = 'cuervo'): #Vemos como el objects.all() sigue siendo prescindible. Al igual que .net, el uso de la s en objects como plural, hace explicito que se trata de una colección de uno o más objetos.
        títulosConCuervo += "\"" + elemento.titulo + "\"" +", " # Usamos un acumulador para formar la lista de libros. Note el escape para las comillas dobles. Recuerde que elemento.titulo es un string o cadena.
    # Con este método, se debe usar el rebanador 'titConCuervo':títulosConCuervo[0:-2] para eliminar el espacio y la coma vacía al final de la cadena que se envia con el diccionario desde la función render.

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(request, 'index.html', context={'num_libros':Libro.objects.all().count(),'num_ejemEspe':num_ejemEspe,'num_ejem_disponibles':num_ejem_dispon,'num_autores':num_autores, 'numero_generos':num_generos, 'totalGeneAutor1':subTotal1, 'conPoe':autoresPoe, 'numTítulosconCuervo':cantTítulosCuervo, 'titConCuervo':títulosConCuervo[0:-2]}, )

class VistaListaDeLibros(generic.ListView):
    model = Libro #De la clase-modelo Libro.

class VistaDetalleDeLibro(generic.DetailView):
    model = Libro
