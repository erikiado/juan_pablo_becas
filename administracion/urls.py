from django.conf.urls import url
from .views import admin_main_dashboard, admin_users_dashboard
from .views import crear_usuario, crear_retroalimentacion  # , revisar_focus_mode

app_name = 'administracion'

# Urls en espanol
urlpatterns = [
    url(r'^principal/', admin_main_dashboard, name='main'),
    url(r'^usuarios/', admin_users_dashboard, name='users'),
    url(r'^crear_usuario/$', crear_usuario, name='crear_usuario'),
    url(r'^crear_retroalimentacion/', crear_retroalimentacion, name='crear_retroalimentacion'),
]
