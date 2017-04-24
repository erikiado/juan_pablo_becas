from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required

from estudios_socioeconomicos.models import Estudio
from perfiles_usuario.utils import is_administrador, is_capturista,\
                                 is_directivo, is_servicios_escolares


@login_required
def home(request):
    """ This view redirects users according to their group.

    TODO:
    Figure out what to do w/users that don't have groups assigned.
    """
    if is_administrador(request.user):
        return redirect('administracion:main_estudios',
                        status_study=Estudio.REVISION)
    if is_capturista(request.user):
        return redirect('captura:estudios')
    if is_directivo(request.user):
        return redirect('indicadores:all')
    if is_servicios_escolares(request.user):
        return redirect('becas:services')
    raise Http404()


def base_files(request, filename):
    location = 'base/' + filename
    return render(request, location, {}, content_type='text/plain')
