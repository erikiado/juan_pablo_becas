from django.contrib.auth.models import User
from django.shortcuts import render


def admin_panel_principal(request):
    '''view para mostrar el panel de control principal
    '''
    return render(request, 'administracion/dashboard_main.html')


def admin_panel_usuarios(request):
    '''view para desplegar los usuarios en el panel de control de usuarios
    '''
    usuarios = User.objects.all()
    return render(request, 'administracion/dashboard_users.html', {'usuarios': usuarios})
