from django.conf.urls import url
from .views import admin_main_dashboard, admin_users_dashboard, \
                   admin_users_create, admin_users_edit, admin_users_edit_form

app_name = 'administracion'

# Urls en espanol
urlpatterns = [
    url(r'^principal/', admin_main_dashboard, name='main'),
    url(r'^usuarios/nuevo/', admin_users_create, name='users_add'),
    url(r'^usuarios/editar/(\d+)/', admin_users_edit_form, name='users_edit_form'),
    url(r'^usuarios/editar/guardar/', admin_users_edit, name='users_edit'),
    url(r'^usuarios/', admin_users_dashboard, name='users'),
]
