from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render

from perfiles_usuario.utils import is_capturista
from estudios_socioeconomicos.models import Estudio


@login_required
#@user_passes_test(is_capturista)
def capturista_dashboard(request):
    """View to render the capturista control dashboard.

       This view shows the list of socio-economic studies that are under review
       and the button to add a new socio-economic study.
       Also shows the edit and see feedback buttons to each socio-economic study
       shown in the list if this exists for the current user (capturist).
    """
    user_id = request.user.id
    estudios = Estudio.objects.filter(status__in=[Estudio.RECHAZADO,Estudio.REVISION,Estudio.BORRADOR],
                                      capturista_id=user_id)
    return render(request, 'captura/dashboard_capturista.html',
                  {'estudios': estudios, 'Estudio':Estudio})
