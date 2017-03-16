from django.conf.urls import url

from .views import capturista_dashboard, capture_study, add_answer_study, remove_answer_study, \
                   create_estudio, show_family, show_economy, show_housing, cycle_sections

app_name = 'captura'

urlpatterns = [
    url(r'^estudios/', capturista_dashboard, name='estudios'),
    url(r'^contestar-estudio/(?P<id_estudio>[0-9]+)/(?P<numero_seccion>[0-9]+)',
        capture_study, name='contestar_estudio'),
    url(r'^agregar-respuesta-estudio/', add_answer_study, name='agregar_respuesta_estudio'),
    url(r'^quitar-respuesta-estudio/', remove_answer_study, name='quitar_respuesta_estudio'),
    url(r'^crear-estudio/', create_estudio, name='create_estudio'),
    url(r'^familia/', show_family, name='family'),
    url(r'^economia/', show_economy, name='income'),
    url(r'^vivienda/', show_housing, name='housing'),
    url(r'^seccion/', cycle_sections, name='sections'),
]
