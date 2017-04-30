from django.conf.urls import url
from .views import focus_mode, download_studies

app_name = 'estudios_socioeconomicos'

urlpatterns = [
    url(r'^estudios/descargar/', download_studies, name='download_studies'),
    url(r'^focus-mode/(?P<id_estudio>[0-9]+)/', focus_mode, name='focus_mode')
]
