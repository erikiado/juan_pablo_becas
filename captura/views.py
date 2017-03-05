from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def estudios(request):
    return render(request, 'administracion/dashboard_users.html')
