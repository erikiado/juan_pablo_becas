from django.conf.urls import url

from .views import logout

app_name = 'tosp_auth'

urlpatterns = [
    url(r'^logout/$', logout, name='logout')
]
