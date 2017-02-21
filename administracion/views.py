from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import FormaUsuario


def crear_usuario(request):
    if request.method == 'POST':
        forma = FormaUsuario(request.POST)
        if forma.is_valid():
            forma.save()
            return HttpResponseRedirect('/administracion/crear_usuario/?us=1')
    else:
        forma = FormaUsuario()
    return render(request, 'crear_usuario.html', {'form': forma})
