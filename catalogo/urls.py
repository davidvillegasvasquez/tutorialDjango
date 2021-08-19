from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), url(r'^libros/$', views.VistaListaDeLibros.as_view(), name='libros'), url(r'^libro/(?P<pk>\d+)$', views.VistaDetalleDeLibro.as_view(), name='libro-detail'), url(r'^autores/$', views.VistaListaDeAutores.as_view(), name='autores'), url(r'^autor/(?P<pk>\d+)$', views.VistaDetalleDeAutor.as_view(), name='autor-detail'),] #Recuerda que con este mapeador estamos creando nuestras urls y emparejando simultaneamente (catalogo/libros y catalogo/libro-detail/número_id. También recuerde que se llegó a este mapeador de la aplicación catalogo, desde la entrada principal a la aplicación, es decir desde el mapeador principal (..., path('catalogo/', include('catalogo.urls'),...)que se encuentra en urls.py en la carpeta de entrada (bibliotecalocal).
#Como VistaDetalleDeLibro.as_view() es una vista genérica que depende del url 'libro', me exige que name sea libro-detail, dónde -detail es reservado por django y libro como minúscula del modelo Libro.

