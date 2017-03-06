from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import FormaCreacionUsuario
from perfiles_usuario.utils import is_administrador


@login_required
@user_passes_test(is_administrador)
def admin_main_dashboard(request):
    """View to render the main control dashboard.

    The content to be shown in this view is the
    list of Estudios (familias).
    """
    return render(request, 'administracion/dashboard_main.html')


@login_required
@user_passes_test(is_administrador)
def admin_users_dashboard(request):
    """View to render the users control dashboard.

    """
    users = User.objects.all()
    create_user_form = FormaCreacionUsuario()

    return render(request, 'administracion/dashboard_users.html',
                  {'all_users': users, 'create_user_form': create_user_form})


@login_required
@user_passes_test(is_administrador)
def admin_users_create(request):
    """ View to create users.

    """
    if request.method == 'POST':
        forma = FormaCreacionUsuario(request.POST)
        if forma.is_valid():
            forma.save()
            return redirect('administracion:users')


@login_required
@user_passes_test(is_administrador)
def admin_focusmode(request):
    """ View to show the focus mode of a certain study.

    """
    return render(request, 'administracion/focus_mode.html')
