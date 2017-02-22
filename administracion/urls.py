from django.conf.urls import url
from .views import crear_usuario

app_name = 'administracion'
urlpatterns = [
    url(r'^crear_usuario/$', crear_usuario, name='crear_usuario'),
]
