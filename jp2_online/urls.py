"""jp2_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url('', include('base.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^administracion/', include('administracion.urls')),
    url(r'^tosp_auth/', include('tosp_auth.urls')),
    url(r'^perfiles-usuario/', include('perfiles_usuario.urls')),
    url(r'^captura/', include('captura.urls')),
    url(r'^indicadores/', include('indicadores.urls')),
    url(r'^becas/', include('becas.urls')),
    url('', include('django.contrib.auth.urls'))
]
