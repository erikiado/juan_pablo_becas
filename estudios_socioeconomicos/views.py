from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator


from perfiles_usuario.utils import is_administrador
from .models import Estudio

decorators = [user_passes_test(User, is_administrador), login_required]


@method_decorator(decorators, name='dispatch')
class PendientesList(ListView):
    """ Shows the list of socio-economic studies that ares
        pending to approval or for review

    """
    model = Estudio
    context_object_name = 'estudios'
    queryset = Estudio.objects.filter(status='revision')
    template_name = 'estudios_socioeconomicos/pendientes.html'


@method_decorator(decorators, name='dispatch')
class RevisionList(ListView):
    """ Shows the list of socio-economic studies under review

    """
    model = Estudio
    context_object_name = 'estudios'
    queryset = Estudio.objects.filter(status='rechazado')
    template_name = 'estudios_socioeconomicos/revision.html'
