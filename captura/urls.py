from django.conf.urls import url

from .views import capture_study, add_answer_study, remove_answer_study, estudios

app_name = 'captura'

urlpatterns = [
    url(r'^contestar-estudio/(?P<id_estudio>[0-9]+)/(?P<numero_seccion>[0-9]+)',
        capture_study, name='contestar_estudio'),
    url(r'^agregar-respuesta-estudio/', add_answer_study, name='agregar_respuesta_estudio'),
    url(r'^quitar-respuesta-estudio/', remove_answer_study, name='quitar_respuesta_estudio'),
    url(r'^estudios/', estudios, name='estudios'),
]
