from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required

from familias.utils import total_egresos_familia, total_ingresos_familia, total_neto_familia
from perfiles_usuario.utils import is_administrador
from estudios_socioeconomicos.models import Estudio, Foto

from .forms import BecaForm


@login_required
def estudios(request):
    """ DUMMY VIEW.

    This functions is currently just being used to test the redirect
    from base.

    TODO: name properly and implement everything
    """
    return render(request, 'layouts/dashboard_base.html')


@login_required
@user_passes_test(is_administrador)
def asignar_beca(request, id_estudio):
    """ Renders the view where the admin assigns the scolarship
    to a family after approving a study.

    TODO: ensure that the study is approved.
    """
    estudio = get_object_or_404(Estudio, pk=id_estudio)
    fotos = Foto.objects.filter(estudio=id_estudio)

    context = {
        'estudio': estudio,
        'total_egresos_familia': total_egresos_familia(estudio.familia.id),
        'total_ingresos_familia': total_ingresos_familia(estudio.familia.id),
        'total_neto_familia': total_neto_familia(estudio.familia.id),
        'fotos': fotos,
        'form': BecaForm()
    }
    return render(request, 'becas/asignar_beca.html', context)
