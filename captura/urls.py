from django.conf.urls import url, include
from rest_framework import routers
from .views import capturista_dashboard, capture_study, add_answer_study, remove_answer_study, \
                   create_estudio, APIQuestionsInformation, APIUploadRetrieveStudy

app_name = 'captura'

router = routers.DefaultRouter()
router.register(r'estudio', APIUploadRetrieveStudy, base_name='estudio')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^estudios/', capturista_dashboard, name='estudios'),
    url(r'^contestar-estudio/(?P<id_estudio>[0-9]+)/(?P<numero_seccion>[0-9]+)',
        capture_study, name='contestar_estudio'),
    url(r'^agregar-respuesta-estudio/', add_answer_study, name='agregar_respuesta_estudio'),
    url(r'^quitar-respuesta-estudio/', remove_answer_study, name='quitar_respuesta_estudio'),
    url(r'^crear-estudio/', create_estudio, name='create_estudio'),
    url(r'^api-obtener-informacion-preguntas/', APIQuestionsInformation.as_view(),
        name='api_obtener_informacion_preguntas'),
]
