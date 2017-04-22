from django.conf.urls import url
from .views import home, base_files, documentation

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^ayuda/', documentation, name='ayuda'),
    url(r'^(?P<filename>(robots.txt)|(humans.txt))$', base_files, name='base_files')
]
