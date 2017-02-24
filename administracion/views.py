from django.contrib.auth.models import User
from django.shortcuts import render


def admin_main_dashboard(request):
    """View to render the main control dashboard.
    """
    return render(request, 'administracion/dashboard_main.html')


def admin_users_dashboard(request):
    """View to render the users control dashboard.
    """
    users = User.objects.all()
    return render(request, 'administracion/dashboard_users.html', {'all_users': users})
