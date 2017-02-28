from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from captura.models import Retroalimentacion
from .forms import FormaCreacionUsuario, FormaRetroalimentacion  # FormaFocusMode


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


def crear_retroalimentacion(request):
    """ View to render form for providing feedback for a study.
    """

    if request.method == 'POST':
        retroalimentacion = Retroalimentacion(usuario=request.user)
        form = FormaRetroalimentacion(request.POST, instance=retroalimentacion)
        if form.is_valid():
            form.save()
            return redirect('administracion:main')
    else:
        form = FormaRetroalimentacion()
    return render(request, 'administracion/retroalimentacion.html', {'form': form})


"""def revisar_focus_mode(request):
def crear_retroalimentacion(request):
    forma = FormaRetroalimentacion

    if request.method == 'POST':
        form = forma(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('retroalimentacion')
    else:
        form = FormaRetroalimentacion()
    return render(request, 'administracion/retroalimentacion.html', {'from': form})
"""
