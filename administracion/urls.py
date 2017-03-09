from django.conf.urls import url
from .views import admin_main_dashboard, admin_users_dashboard, admin_users_create, list_studies

app_name = 'administracion'

# Urls en espanol
urlpatterns = [
    url(r'^home/', admin_main_dashboard, name='main'),
    url(r'^usuarios/', admin_users_dashboard, name='users'),
    url(r'^usuarios/nuevo/', admin_users_create, name='users_add'),
    url(r'^principal/(?P<status_study>[\w\-]+)/$', list_studies, name='main_estudios'),
]
