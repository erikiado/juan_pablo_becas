from django.conf.urls import url
from .views import focus_mode

app_name = 'estudios_socioeconomicos'

urlpatterns = [
    url(r'^focus-mode/(?P<id_estudio>[0-9]+)/', focus_mode, name='focus_mode')
]