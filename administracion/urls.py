from django.conf.urls import url
from .views import admin_main_dashboard, admin_users_dashboard

app_name = 'administracion'

# Urls en espanol
urlpatterns = [
    url(r'^principal/', admin_main_dashboard, name='main'),
    url(r'^usuarios/', admin_users_dashboard, name='users')
]
