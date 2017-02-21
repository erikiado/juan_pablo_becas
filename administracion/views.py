from django.contrib.auth.models import User
from django.shortcuts import render


# view para mostrar el panel de control principal
def admin_panel_principal(request):
    return render(request, 'administracion/dashboard_main.html')


# view para desplegar los usuarios en el panel de control de usuarios
def admin_panel_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'administracion/dashboard_users.html', {'usuarios': usuarios})
