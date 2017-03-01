from django.conf.urls import url

from .views import revision_list, pendientes_list

app_name = 'estudios_socioeconomicos'

urlpatterns = [
    url(r'^revision/$', revision_list, name='revision'),
    url(r'^pendientes/$', pendientes_list, name='pendientes'),
]
