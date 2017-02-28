from django.conf.urls import url

from .views import PendientesList, RevisionList

app_name = 'estudios_socioeconomicos'

urlpatterns = [
    url(r'^pendientes/$', PendientesList.as_view(), name='pendientes'),
    url(r'^revision/$', RevisionList.as_view(), name='revision'),
]
