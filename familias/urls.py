from django.conf.urls import url
from .views import families_directory, family_member

app_name = 'familias'

# URLS en español
urlpatterns = [
    url(r'^todos/', families_directory, name='all'),
    url(r'^integrante/', family_member, name='member'),
]
