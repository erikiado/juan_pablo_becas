from django.conf.urls import url
from .views import estudios

app_name = 'becas'

# Urls en espanol
urlpatterns = [
    url(r'^estudios/', estudios, name='services'),
]
