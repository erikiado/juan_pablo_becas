from django.conf.urls import url
from .views import crear_usuario

urlpatterns = [
    url(r'^crear_usuario/$', views.crear_usuario, name='crear_usuario'),
]
