from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from perfiles_usuario.utils import is_capturista
from estudios_socioeconomicos.models import Estudio


@login_required
@user_passes_test(is_capturista)
def capturista_dashboard(request):
    """View to render the capturista control dashboard.

       This view shows the list of socio-economic studies that are under review
       and the button to add a new socio-economic study.
       Also shows the edit and see feedback buttons to each socio-economic study
       shown in the list if this exists for the current user (capturist).
    """
    estudios = []
    iduser = request.user.id
    rechazados = Estudio.objects.filter(status='rechazado')
    for estudio in rechazados:
        if estudio.capturista_id == iduser:
            estudios.append(estudio)
    return render(request, 'captura/dashboard_capturista.html',
                  {'estudios': estudios})
