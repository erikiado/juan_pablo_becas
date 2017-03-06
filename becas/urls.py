from django.conf.urls import url
from .views import reinscription_studies_left

app_name = 'becas'

# URLS en español
urlpatterns = [
    url(r'^estudios/', reinscription_studies_left, name='services'),
]