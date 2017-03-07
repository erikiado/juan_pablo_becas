from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from perfiles_usuario.utils import is_capturista
from estudios_socioeconomicos.models import Estudio


@login_required
@user_passes_test(is_capturista)
def capturista_dashboard(request):
    """View to render the capturista control dashboard.

    """
    estudios = Estudio.objects.filter(status='rechazado')
    return render(request, 'captura/dashboard_capturista.html',
                  {'estudios': estudios})
