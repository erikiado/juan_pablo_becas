from django.conf.urls import url
from .views import estado_civil, breakdown_alumnos, estudios_padres, edad_padres, \
                   ocupaciones, ingreso_mensual, localidad, sacramentos, \
                   becas

app_name = 'indicadores'

# Urls en espanol
urlpatterns = [
    url(r'^estado_civil/', estado_civil, name='estado_civil'),
    url(r'^breakdown_alumnos/', breakdown_alumnos, name='breakdown_alumnos'),
    url(r'^estudios_padres/', estudios_padres, name='estudios_padres'),
    url(r'^edad_padres/', edad_padres, name='edad_padres'),
    url(r'^ocupaciones/', ocupaciones, name='ocupaciones'),
    url(r'^ingreso_mensual/', ingreso_mensual, name='ingreso_mensual'),
    url(r'^localidad/', localidad, name='localidad'),
    url(r'^sacramentos/', sacramentos, name='sacramentos'),
    url(r'^becas/', becas, name='becas')
]
