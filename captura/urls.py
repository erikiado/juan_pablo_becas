from django.conf.urls import url
from .views import capturista_dashboard

app_name = 'captura'


urlpatterns = [
    url(r'^capturista/', capturista_dashboard, name='capturista_dashboard'),
]
