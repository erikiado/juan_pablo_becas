from django.conf.urls import url
from .views import estudios

app_name = 'captura'

# Urls en espanol
urlpatterns = [
    url(r'^estudios/', estudios, name='estudios'),
]
