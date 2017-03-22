from django.conf.urls import url
from .views import all_indicadores, show_indicator

app_name = 'indicadores'

# Urls en espanol
urlpatterns = [
    url(r'^todos/', all_indicadores, name='all'),
    url(r'^', show_indicator, name='detail'),
]
