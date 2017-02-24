from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import FormaCreacionUsuario


def admin_main_dashboard(request):
    """View to render the main control dashboard.
    """
    return render(request, 'administracion/dashboard_main.html')


def admin_users_dashboard(request):
    """View to render the users control dashboard.
    """
    users = User.objects.all()
    create_user_form = FormaCreacionUsuario()
    return render(request, 'administracion/dashboard_users.html',
                  {'all_users': users, 'create_user_form': create_user_form})


def admin_users_create(request):
    """ View to create users.

    TODO: select proper template, and redirection url.
    """
    if request.method == 'POST':
        forma = FormaCreacionUsuario(request.POST)
        if forma.is_valid():
            forma.save()
            return redirect('administracion:users')
