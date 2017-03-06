from django.conf.urls import url
from .views import admin_main_dashboard, admin_users_dashboard, admin_users_create, admin_focusmode

app_name = 'administracion'

# Urls en espanol
urlpatterns = [
    url(r'^principal/', admin_main_dashboard, name='main'),
    url(r'^usuarios/nuevo/', admin_users_create, name='users_add'),
    url(r'^usuarios/', admin_users_dashboard, name='users'),
    url(r'^estudios/', admin_focusmode, name='focus'),
]
