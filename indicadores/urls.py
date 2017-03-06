from django.conf.urls import url
from .views import all_indicators, show_indicator

app_name = 'indicadores'

# URLS en español
urlpatterns = [
    url(r'^todos/', all_indicators, name='all'),
    url(r'^', show_indicator, name='detail'),
]
