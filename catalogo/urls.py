from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), url(r'^libros/$', views.VistaListaDeLibros.as_view(), name='libros'), url(r'^libro/(?P<pk>\d+)$', views.VistaDetalleDeLibro.as_view(), name='libro-detail'), url(r'^autores/$', views.VistaListaDeAutores.as_view(), name='autores'), url(r'^autor/(?P<pk>\d+)$', views.VistaDetalleDeAutor.as_view(), name='autor-detail'),] #Recuerda que con este mapeador estamos creando nuestras urls y emparejando simultaneamente (catalogo/libros y catalogo/libro-detail/número_id. También recuerde que se llegó a este mapeador de la aplicación catalogo, desde la entrada principal a la aplicación, es decir desde el mapeador principal (..., path('catalogo/', include('catalogo.urls'),...)que se encuentra en urls.py en la carpeta de entrada (bibliotecalocal).
#Como VistaDetalleDeLibro.as_view() es una vista genérica que depende del url 'libro', me exige que name sea libro-detail, dónde -detail es reservado por django y libro como minúscula del modelo Libro.

urlpatterns += [
    path('librosUsuario/', views.VistaEjemplaresParaLosUsuarios.as_view(), name='VistaUsuarios'),
] 

urlpatterns += [
    path('bibliotecariosPermiso1/', views.VistaEjemplaresParaBibliotecarios1.as_view(), name='VistaBibliotecarios1'),
]

urlpatterns += [
    path('bibliotecariosPermiso2/', views.VistaEjemplaresParaBibliotecarios2.as_view(), name='VistaBibliotecarios2'),
]

urlpatterns += [
    path('libro/<uuid:pk>/renovar/', views.RenovacionLibroPorLibrero, name='librosRenovPorLibrero'),
]

#Como se vió anteriormente, el parámetro name de la función path con los valores autor-create, autor-update, nombreCampo-delete, tienen la sintaxis nombreCampo-tipoDeOperación, dónde tipoDeOperación tiene los nombres reservados create, update y delete que los emparejará automaticamente con los nombres reservados de plantillas, nombreCampo_form.html (autor_form.html para este ejemplo) para las operaciones de creación y actualización, y nombreCampo_confirm_delete.html, para el borrado (parametro name=autor-delete en la función path).
urlpatterns += [
    path('autor/crear/', views.CrearAutor.as_view(), name='autor-create'),
    path('autor/<int:pk>/actualizar/', views.ActualizarAutor.as_view(), name='autor-update'),
    path('autor/<int:pk>/borrar/', views.BorrarAutor.as_view(), name='autor-delete'),
]

urlpatterns += [
    path('libro/crear/', views.CrearLibro.as_view(), name='libro-create'),
    path('libro/<int:pk>/actualizar/', views.ActualizarLibro.as_view(), name='libro-update'),
    path('libro/<int:pk>/borrar/', views.BorrarLibro.as_view(), name='libro-delete'),
]
