from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test


from perfiles_usuario.utils import is_administrador
from .models import Estudio


@login_required
@user_passes_test(User, is_administrador)
def pendientes_list(request):
    estudios = Estudio.objects.filter(status='revision')
    contexto = {'estudios': estudios}
    return render(request, 'estudios_socioeconomicos/pendientes.html', contexto)


@login_required
@user_passes_test(User, is_administrador)
def revision_list(request):
    estudios = Estudio.objects.filter(status='rechazado')
    contexto = {'estudios': estudios}
    return render(request, 'estudios_socioeconomicos/revision.html', contexto)
