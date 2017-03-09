from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import FormaCreacionUsuario
from perfiles_usuario.utils import is_administrador
from estudios_socioeconomicos.models import Estudio


def admin_main_dashboard(request):
    """View to render the main control dashboard.
    """
    return render(request, 'administracion/dashboard_main.html')


def admin_users_dashboard(request):
    """View to render the users control dashboard.
    """
    users = User.objects.all()
    return render(request, 'administracion/dashboard_users.html', {'all_users': users})


def crear_usuario(request):
    """ View to create users.

    TODO: select proper template, and redirection url.
    """
    if request.method == 'POST':
        forma = FormaCreacionUsuario(request.POST)
        if forma.is_valid():
            forma.save()
            return redirect('administracion:users')
    else:
        forma = FormaCreacionUsuario()
    return render(request, 'crear_usuario.html', {'form': forma})


@login_required
@user_passes_test(User, is_administrador)
def main(request, status_study):
    estudios = Estudio.objects.filter(status=status_study)
    contexto = {'estudios': estudios, 'estado': status_study, 'Estudio': Estudio}
    return render(request, 'estudios_socioeconomicos/principal.html', contexto)
