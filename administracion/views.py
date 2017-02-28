from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import FormaCreacionUsuario, UserUpdateForm
from perfiles_usuario.utils import is_administrador
from django.http import HttpResponse
import json
from django.template.loader import render_to_string

@login_required
@user_passes_test(is_administrador)
def admin_main_dashboard(request):
    """View to render the main control dashboard.

    """
    return render(request, 'administracion/dashboard_main.html')


@login_required
@user_passes_test(is_administrador)
def admin_users_dashboard(request):
    """View to render the users control dashboard.

    """
    users = User.objects.all()
    create_user_form = FormaCreacionUsuario()

    return render(request, 'administracion/dashboard_users.html',
                  {'all_users': users, 'create_user_form': create_user_form})


@login_required
@user_passes_test(is_administrador)
def admin_users_create(request):
    """ View to create users.

    """
    if request.method == 'POST':
        forma = FormaCreacionUsuario(request.POST)
        if forma.is_valid():
            forma.save()
            return redirect('administracion:users')

@login_required
@user_passes_test(is_administrador)
def admin_users_edit_form(request, user_id):
    """ View to send the form to edit users.

    """
    # if request.is_ajax():
    user = User.objects.get(pk=user_id)
    form = UserUpdateForm(instance=user,initial={'rol_usuario': user.groups.all()[0].name})
    return render(request,'administracion/user_form.html',{'user_form':form, 'from_user':user})

@login_required
@user_passes_test(is_administrador)
def admin_users_edit(request):
    """ View to edit users.

    """
    # user = User.objects.get(pk=1)
    # print(request)
    if request.method == 'POST':
        user_id = request.POST['user_id']
        instance = User.objects.get(pk=user_id)
        form = UserUpdateForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('administracion:users')

    # print(user)
        # user_form = {}
        # user_form["errors"] = form.errors
        # user_form["fields"] = {}
        # for field in form:
            # user_form["fields"][field] = field
        # html = render_to_string('administracion/user_form.html', {'user_form': user_form}, request=request)
        # if forma.is_valid():
            # forma.save()
        # return HttpResponse(json.dumps({'name': forma}), content_type="application/json")
