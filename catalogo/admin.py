from django.contrib import admin
from .models import Autor, Genero, Libro, EjemplarEspecifico, Lenguaje

# Primero se deben definir los modelos admin para luego registrarlos abajo, si no dara excepción por haber "puesto la carreta delante de los caballos".

class EjemplarEspecificoInline(admin.TabularInline):
    model = EjemplarEspecifico

class AutorAdmin(admin.ModelAdmin):
    # Para mostrar en columnas los campos de la tabla Autor (configurar la vista de lista usando list_display):
    #list_display = ('apellido', 'nombre', 'fecha_nacimiento', 'fecha_muerte')
    # El atributo fields,lista sólo los campos que se van a desplegar en el formulario, en orden. Los que están entre paréntesis los pone en columna(vertical):
    fields = ['nombre', 'apellido', ('fecha_nacimiento', 'fecha_muerte')]
    #El atributo exclude excluye campos, claro si se usa no puede ser incluido en un fields:
    #exclude = ['nombre']

# Con el uso de decoradores (@admin.register(nombredelmodelo)) puedo registrar antes de definir.
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'display_genero')
    inlines = [EjemplarEspecificoInline]

@admin.register(EjemplarEspecifico)
class EjemplarEspecificoAdmin(admin.ModelAdmin):
    list_display = ('libro', 'status', 'prestatario', 'campoConstante', 'devolucion', 'id')  #Si desconecto esta línea comentandola, solo me pondrá el títula de la columna "Ejemplar Específico", y los item con su id y nombre del libro pegados.
    list_filter = ('status', 'devolucion')
    fieldsets = (
        (None, {
            'fields': ('libro', 'impresion', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'devolucion', 'prestatario')
        }),
    ) # La propiedad Availability se refiere a que la columna del campo en la plantilla no está bloqueada, inhabilitada. Aquí no importa el orden en que esté en la lista, pues es un atributo, no un objeto-cadena visible en la pantalla.

# Register your models here.

# admin.site.register(Libro) #Como usé decoradores para registrar este módelo, no hace falta esta línea. Puse "la carreta delante de los caballos".
# admin.site.register(Autor)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Genero)
# admin.site.register(EjemplarEspecifico)
admin.site.register(Lenguaje)

