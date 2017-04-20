from django.conf.urls import url
from .views import estudios, asignar_beca, carta_beca

app_name = 'becas'

# Urls en espanol
urlpatterns = [
    url(r'^estudios/', estudios, name='services'),
    url(r'^asignar-beca/(?P<id_estudio>[0-9]+)/', asignar_beca, name='asignar_beca'),
    url(r'^genera/', carta_beca)
]
