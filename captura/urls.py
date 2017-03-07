from django.conf.urls import url

from .views import capturista_dashboard

app_name = 'captura'


urlpatterns = [
    url(r'^estudios/', capturista_dashboard, name='estudios'),
]
