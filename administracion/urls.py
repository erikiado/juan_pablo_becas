from django.conf.urls import url
from .views import admin_panel_principal, admin_panel_usuarios

urlpatterns = [
    url(r'^panel/', admin_panel_principal, name='administracion_principal'),
    url(r'^usuarios/', admin_panel_usuarios, name='administracion_usuarios')
]
