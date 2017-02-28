from django.conf.urls import url

from .views import ObtainAuthToken

app_name = 'perfiles_usuario'

urlpatterns = [
    url(r'^obtain-auth-token/', ObtainAuthToken.as_view(), name='obtain_auth_token'),
]
