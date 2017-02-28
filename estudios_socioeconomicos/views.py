from django.shortcuts import render
from django.views.generic import ListView

from .models import Estudio


class pendientes_list(ListView):
    """ Shows the list of socio-economic studies that are
        pending to approval or for review

    """
    model = Estudio
    context_object_name = 'estudios'
    queryset = Estudio.objects.filter(status='revision')
    template_name = 'estudios_socioeconomicos/pendientes.html'


class revision_list(ListView):
    """ Shows the list of socio-economic studies under review

    """
    model = Estudio
    context_object_name = 'estudios'
    queryset = Estudio.objects.filter(status='rechazado')
    template_name = 'estudios_socioeconomicos/revision.html'
