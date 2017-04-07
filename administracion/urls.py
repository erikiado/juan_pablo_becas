from django.conf.urls import url
from .views import admin_main_dashboard, admin_users_dashboard, \
                   admin_users_create, admin_users_edit, admin_users_edit_form, \
                   admin_users_delete_modal, admin_users_delete, list_studies, \
                   focus_mode, reject_study, search_students, detail_student

app_name = 'administracion'

# Urls en espanol
urlpatterns = [
    url(r'^principal/$', admin_main_dashboard, name='main'),
    url(r'^usuarios/nuevo/', admin_users_create, name='users_add'),
    url(r'^usuarios/editar/(\d+)/', admin_users_edit_form, name='users_edit_form'),
    url(r'^usuarios/editar/guardar/', admin_users_edit, name='users_edit'),
    url(r'^usuarios/borrar/(\d+)/', admin_users_delete_modal, name='users_delete_modal'),
    url(r'^usuarios/borrar/confirmar/', admin_users_delete, name='users_delete'),
    url(r'^usuarios/', admin_users_dashboard, name='users'),
    url(r'^principal/(?P<status_study>[\w\-]+)/$', list_studies, name='main_estudios'),
    url(r'^principal/(?P<study_id>[\w\-]+)/detalle', focus_mode, name='focus_mode'),
    url(r'^estudio/rechazar/$', reject_study, name='reject_study'),
    url(r'^busqueda/', search_students, name='search_students'),
    url(r'^detalle-alumno/(?P<id_alumno>[0-9]+)', detail_student, name='detail_student'),
]
