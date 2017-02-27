from django.conf.urls import url

from .views import pendientes_list, revision_list

app_name = 'estudios_socioeconomicos'

urlpatterns = [
    url(r'^pendientes/$', pendientes_list.as_view(), name='pendientes'),
    url(r'^revision/$', revision_list.as_view(), name='revision'),
]
