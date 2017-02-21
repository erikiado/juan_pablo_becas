from django.conf.urls import url
from .views import admin_dashboard, admin_users

urlpatterns = [
    url(r'^panel/', admin_dashboard, name='administracion_panel'),
    url(r'^usuarios/', admin_users, name='administracion_usuarios')
]
