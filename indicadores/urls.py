from django.conf.urls import url
from .views import all_indicadores, specific_indicador

app_name = 'indicadores'

# Urls en espanol
urlpatterns = [
    url(r'^todos/', all_indicadores, name='all'),
    url(r'^(?P<indicador>\w+)/', specific_indicador, name='specific_indicador')
]
