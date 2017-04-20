from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http.response import HttpResponseBadRequest

from familias.utils import total_egresos_familia, total_ingresos_familia, total_neto_familia
from familias.models import Integrante
from perfiles_usuario.utils import is_administrador
from estudios_socioeconomicos.models import Estudio, Foto

from .forms import BecaForm
from .models import Beca


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
        'fotos': fotos
    }
    if request.method == 'GET':
        context['form'] = BecaForm()
        return render(request, 'becas/asignar_beca.html', context)
    elif request.method == 'POST':
        form = BecaForm(request.POST)
        if form.is_valid():
            percentage = float(form.cleaned_data['porcentaje']) / 100.
            # create scolarships for active students
            integrantes = Integrante.objects.filter(familia__pk=estudio.familia.pk, activo=True)
            for integrante in filter(lambda x: hasattr(x, 'alumno_integrante'), integrantes):
                Beca.objects.create(alumno=integrante.alumno_integrante,
                                    monto=1500. - (1500. * percentage))
            return redirect('becas:asignar_beca', id_estudio=id_estudio)
        else:
            context['form'] = form
            return render(request, 'becas/asignar_beca.html', context)
    return HttpResponseBadRequest()
