from django.conf.urls import url

from . import views

app_name = 'captura'

urlpatterns = [
    url(r'^contestar-estudio/(?P<id_estudio>[0-9]+)/(?P<numero_seccion>[0-9]+)',
        views.capture_study, name='contestar_estudio'),
    url(r'^agregar-respuesta-estudio/', views.add_answer_study, name='agregar_respuesta_estudio'),
    url(r'^quitar-respuesta-estudio/', views.remove_answer_study, name='quitar_respuesta_estudio'),
    url(r'^estudios/', views.estudios, name='estudios'),
]
