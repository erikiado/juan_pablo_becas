from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import FormaCreacionUsuario


def crear_usuario(request):
    if request.method == 'POST':
        forma = FormaCreacionUsuario(request.POST)
        if forma.is_valid():
            forma.save()
            return HttpResponseRedirect('/administracion/crear_usuario/?us=1')
    else:
        forma = FormaCreacionUsuario()
    return render(request, 'crear_usuario.html', {'form': forma})
