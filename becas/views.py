from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http.response import HttpResponseBadRequest
from django.http import HttpResponse

from familias.utils import total_egresos_familia, total_ingresos_familia, total_neto_familia
from familias.models import Integrante
from perfiles_usuario.utils import is_administrador
from estudios_socioeconomicos.models import Estudio, Foto

from .forms import BecaForm
from .models import Beca
from .utils import generate_letter


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
    """ GET: Renders the view where the admin assigns the scholarship
    to a family after approving a study.

    POST: Validates the form and creates scholarships for all
    students associated to the study.
    """
    estudio = get_object_or_404(Estudio, pk=id_estudio, status=Estudio.APROBADO)
    fotos = Foto.objects.filter(estudio=id_estudio)
    integrantes = Integrante.objects.filter(familia__pk=estudio.familia.pk, activo=True)
    integrantes = filter(lambda x: hasattr(x, 'alumno_integrante'), integrantes)
    context = {
        'estudio': estudio,
        'total_egresos_familia': total_egresos_familia(estudio.familia.id),
        'total_ingresos_familia': total_ingresos_familia(estudio.familia.id),
        'total_neto_familia': total_neto_familia(estudio.familia.id),
        'fotos': fotos,
        'integrantes': integrantes
    }
    if request.method == 'GET':
        context['form'] = BecaForm()
        return render(request, 'becas/asignar_beca.html', context)
    elif request.method == 'POST':
        form = BecaForm(request.POST)
        if form.is_valid():
            percentage = form.cleaned_data['porcentaje']
            # create scholarships for active students
            for integrante in integrantes:
                Beca.objects.create(alumno=integrante.alumno_integrante,
                                    porcentaje=percentage)
            return redirect('estudios_socioeconomicos:focus_mode', id_estudio=id_estudio)
        else:
            context['form'] = form
            return render(request, 'becas/asignar_beca.html', context)
    return HttpResponseBadRequest()


def carta_beca(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    generate_letter(response)
    return response
