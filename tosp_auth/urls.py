from django.conf.urls import url

from .views import logout, login

app_name = 'tosp_auth'

urlpatterns = [
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login')
]
