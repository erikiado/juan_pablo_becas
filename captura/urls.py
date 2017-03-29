from django.conf.urls import url, include
from rest_framework import routers
from .views import capturista_dashboard, capture_study, add_answer_study, remove_answer_study, \
                   create_estudio, edit_familia, integrantes, create_integrante, edit_integrante, \
                   create_alumno, create_tutor, APIQuestionsInformation, APIUploadRetrieveStudy

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
    url(r'^familia/(?P<id_familia>[0-9]+)', edit_familia, name='familia'),
    url(r'^familia/integrantes/(?P<id_familia>[0-9]+)', integrantes, name='integrantes'),
    url(r'^familia/create-integrante/(?P<id_familia>[0-9]+)',
        create_integrante,
        name='create_integrante'),
    url(r'^integrante/create-alumno/(?P<id_integrante>[0-9]+)',
        create_alumno,
        name='create_alumno'),
    url(r'^integrante/create-tutor/(?P<id_integrante>[0-9]+)',
        create_tutor,
        name='create_tutor'),
    url(r'^integrante/(?P<id_integrante>[0-9]+)', edit_integrante, name='integrante'),
    url(r'^api-obtener-informacion-preguntas/', APIQuestionsInformation.as_view(),
        name='api_obtener_informacion_preguntas'),
]
