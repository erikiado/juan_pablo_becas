from django.conf.urls import url, include
from rest_framework import routers
from .views import capturista_dashboard, capture_study, add_answer_study, remove_answer_study, \
                   create_estudio, edit_familia, list_integrantes, create_edit_integrante, \
                   APIQuestionsInformation, APIUploadRetrieveStudy, estudio_delete_modal, \
                   estudio_delete, get_form_edit_integrante, APIOficioInformation, \
                   APIEscuelaInformation, APIUploadRetrieveImages, update_create_transaccion, \
                   delete_transaccion, list_transacciones, update_transaccion_modal, \
                   get_form_delete_integrante, delete_integrante, recover_estudios, \
                   estudio_recover_modal, estudio_recover

app_name = 'captura'

router = routers.DefaultRouter()
router.register(r'estudio', APIUploadRetrieveStudy, base_name='estudio')
router.register(r'imagenes/(?P<id_estudio>[0-9]+)/', APIUploadRetrieveImages, base_name='imagenes')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^estudios/', capturista_dashboard, name='estudios'),
    url(r'^contestar-estudio/(?P<id_estudio>[0-9]+)/(?P<numero_seccion>[0-9]+)',
        capture_study, name='contestar_estudio'),
    url(r'^agregar-respuesta-estudio/', add_answer_study, name='agregar_respuesta_estudio'),
    url(r'^quitar-respuesta-estudio/', remove_answer_study, name='quitar_respuesta_estudio'),
    url(r'^crear-estudio/', create_estudio, name='create_estudio'),
    url(r'^borrar-estudio/(?P<id_estudio>[0-9]+)/',
        estudio_delete_modal,
        name='estudio_delete_modal'),
    url(r'^borrar-estudio/confirmar/',
        estudio_delete, name='estudio_delete'),
    url(r'^familia/(?P<id_familia>[0-9]+)',
        edit_familia, name='familia'),
    url(r'^familia/integrantes/(?P<id_familia>[0-9]+)',
        list_integrantes, name='list_integrantes'),
    url(r'^familia/create-integrante/(?P<id_familia>[0-9]+)',
        create_edit_integrante, name='create_integrante'),
    url(r'^familia/edit-integrante/(?P<id_integrante>[0-9]+)',
        get_form_edit_integrante, name='form_edit_integrante'),
    url(r'^create-transaccion/(?P<id_familia>[0-9]+)',
        update_create_transaccion,
        name='create_transaccion'),
    url(r'^editar-transaccion-modal/(?P<id_transaccion>[0-9]+)',
        update_transaccion_modal,
        name='update_transaccion_modal'),
    url(r'^borrar-transaccion/(?P<id_transaccion>[0-9]+)',
        delete_transaccion,
        name='delete_transaccion'),
    url(r'^familia/transacciones/(?P<id_familia>[0-9]+)',
        list_transacciones,
        name='list_transacciones'),
    url(r'^api-obtener-informacion-preguntas/',
        APIQuestionsInformation.as_view(),
        name='api_obtener_informacion_preguntas'),
    url(r'api-obtener-informacion-escuelas/', APIEscuelaInformation.as_view(),
        name='api_obtener_informacion_escuelas'),
    url(r'api-obtener-informacion-oficios/', APIOficioInformation.as_view(),
        name='api_obtener_informacion_oficios'),
    url(r'borrar-integrante/(?P<id_integrante>[0-9]+)',
        get_form_delete_integrante, name='form_delete_integrante'),
    url(r'borrar-integrante/confirmar/(?P<id_integrante>[0-9]+)',
        delete_integrante, name='delete_integrante'),
    url(r'recuperar-estudios/$', recover_estudios,
        name='recover_studies'),
    url(r'recuperar-estudio/(?P<id_estudio>[0-9]+)', estudio_recover_modal, 
        name='estudio_recover_modal'),
    url(r'recuperar-estudio/confirmar/', estudio_recover,
        name='estudio_recover'),
]
