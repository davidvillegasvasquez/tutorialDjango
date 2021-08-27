"""bibliotecalocal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), path('catalogo/', include('catalogo.urls')),
    path('', RedirectView.as_view(url='/catalogo/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Add Django site authentication urls (for login, logout, password management)

urlpatterns += [
    path('cuentas/', include('django.contrib.auth.urls')),
] #Es lo mismo que agregarla arriba, entre los corchetes.


#El path('', RedirectView.as_view... tenía un slash entre las comillas, lo cual me arrojaba la excepción:
# WARNINGS: ?: (urls.W002) Your URL pattern '/' has a route beginning with a '/'. Remove this slash as it is 
# unnecessary. If this pattern is targeted in an include(), ensure the include() pattern has a trailing '/'.
 

