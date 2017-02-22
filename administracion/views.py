from django.contrib.auth.models import User
from django.shortcuts import render


def admin_panel_principal(request):
    '''View to render the main control dashboard.
    '''
    return render(request, 'administracion/dashboard_main.html')


def admin_panel_usuarios(request):
    '''View to render the users control dashboard.
    '''
    usuarios = User.objects.all()
    return render(request, 'administracion/dashboard_users.html', {'usuarios': usuarios})
