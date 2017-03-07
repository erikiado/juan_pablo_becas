from django.conf.urls import url
from .views import pending_studies, show_family, show_economy, show_housing, cycle_sections

app_name = 'captura'

# URLS en español
urlpatterns = [
    url(r'^estudios/', pending_studies, name='estudios'),
    url(r'^familia/', show_family, name='family'),
    url(r'^economia/', show_economy, name='income'),
    url(r'^vivienda/', show_housing, name='housing'),
    url(r'^seccion/', cycle_sections, name='sections'),
]
