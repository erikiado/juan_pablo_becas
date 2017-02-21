from django.contrib.auth.models import User
from django.shortcuts import render


# Create your views here.
def admin_dashboard(request):
    return render(request, 'administracion/dashboard_main.html')


def admin_users(request):
    usuarios = User.objects.all()
    return render(request, 'administracion/user_admin.html', {'usuarios': usuarios})
