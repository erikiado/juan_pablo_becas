from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import FormaUsuario

def crear_usuario(request):
    # no se si sea necesario
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        forma = FormaUsuario(request.POST)
        # si la forma contiene todos los campos es valida
        if forma.is_valid():
            first_name = forma.cleaned_data['first_name']
            last_name   = forma.cleaned_data['last_name']
            email       = forma.cleaned_data['email']
            password    = forma.cleaned_data['password']
            rol_usuario = forma.cleaned_data['rol_usuario']
            forma.save()
            # Direccionar a dashboard 'administracion'
            # Checar reverse de urls
            return HttpResponseRedirect('/administracion/crear_usuario/?us=1')

    # if a GET  we'll create a blank form
    else:
        forma = FormaUsuario()

    return render(request, 'crear_usuario.html', {'form': forma})