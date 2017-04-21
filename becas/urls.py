from django.conf.urls import url
from .views import estudios, asignar_beca, genera_carta

app_name = 'becas'

# Urls en espanol
urlpatterns = [
    url(r'^estudios/', estudios, name='services'),
    url(r'^asignar-beca/(?P<id_estudio>[0-9]+)/', asignar_beca, name='asignar_beca'),
    url(r'^genera-carta/(?P<id_alumno>[0-9]+)/', genera_carta, name='genera_carta'),
]
