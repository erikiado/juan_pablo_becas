from django.conf.urls import url
from .views import focus_mode, accept_study, reject_study

app_name = 'estudios_socioeconomicos'

urlpatterns = [
    url(r'^focus-mode/(?P<id_estudio>[0-9]+)/', focus_mode, name='focus_mode'),
    url(r'^estudio/rechazar/$', reject_study, name='reject_study'),
    url(r'^estudio/aceptar/(?P<id_estudio>[0-9]+)/', accept_study, name='accept_study'),
]
