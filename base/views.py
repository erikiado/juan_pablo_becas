from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from perfiles_usuario.utils import is_administrador, is_capturista,\
                                 is_directivo, is_servicios_escolares


@login_required
def home(request):
    if is_administrador(request.user):
        return redirect('administracion:main')
    if is_capturista(request.user):
        return redirect('captura:estudios')
    if is_directivo(request.user):
        return redirect('indicadores:all')
    if is_servicios_escolares(request.user):
        return redirect('becas:services')


def base_files(request, filename):
    location = "base/" + filename
    return render(request, location, {}, content_type="text/plain")
