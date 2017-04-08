from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from perfiles_usuario.utils import is_capturista, is_administrador
from familias.models import Familia, Alumno, Tutor, Integrante
from indicadores.models import Transaccion, Periodo, Oficio
from .models import Estudio, Foto


@login_required
def focus_mode(request, id_estudio):
    context = {}

    estudio = get_object_or_404(Estudio.objects.filter(pk=id_estudio))

    if is_capturista(request.user):
        get_object_or_404(Estudio.objects.filter(pk=id_estudio), capturista=request.user.capturista)


    integrantes = Integrante.objects.filter(familia=estudio.familia).select_related()
    fotos = Foto.objects.filter(estudio=id_estudio)
    context['estudio'] = estudio
    context['integrantes'] = integrantes
    context['fotos'] = fotos

    return render(
        request,
        'estudios_socioeconomicos/focus_mode.html',
        context)