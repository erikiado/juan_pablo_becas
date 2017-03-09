from django.conf.urls import url
from .views import all_indicadores

app_name = 'indicadores'

# Urls en espanol
urlpatterns = [
    url(r'^todos/', all_indicadores, name='all'),
]
