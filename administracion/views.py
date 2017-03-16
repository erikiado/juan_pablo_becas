from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import UserForm, DeleteUserForm
from perfiles_usuario.utils import is_administrador


@login_required
@user_passes_test(is_administrador)
def admin_main_dashboard(request):
    """View to render the main control dashboard.

    The content to be shown in this view is the
    list of Estudios (familias).
    """
    return render(request, 'administracion/dashboard_main.html')


@login_required
@user_passes_test(is_administrador)
def admin_users_dashboard(request):
    """View to render the users control dashboard.

    """
    users = User.objects.all()
    create_user_form = UserForm()

    return render(request, 'administracion/dashboard_users.html',
                  {'all_users': users, 'create_user_form': create_user_form})


@login_required
@user_passes_test(is_administrador)
def admin_users_create(request):
    """ View to create users.

    """
    if request.method == 'POST':
        forma = UserForm(request.POST)
        if forma.is_valid():
            forma.save()
            return redirect('administracion:users')


@login_required
@user_passes_test(is_administrador)
def admin_focus_mode(request):
    """ View to show the focus mode of a certain study.

    TODO. This is a dummy view, therefore it may
    be changed in the future.
    """
    return render(request, 'administracion/focus_mode.html')


@login_required
@user_passes_test(is_administrador)
def admin_users_edit_form(request, user_id):
    """ View to send the form to edit users.

    """
    if request.is_ajax():
        user = User.objects.get(pk=user_id)
        form = UserForm(instance=user, initial={'rol_usuario': user.groups.all()[0].name})
        return render(request, 'administracion/user_form.html',
                      {'user_form': form, 'from_user': user})


@login_required
@user_passes_test(is_administrador)
def admin_users_edit(request):
    """ View to edit users.

    """
    if request.method == 'POST':
        user_id = request.POST['user_id']
        instance = User.objects.get(pk=user_id)
        form = UserForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('administracion:users')


@login_required
@user_passes_test(is_administrador)
def admin_users_delete_modal(request, user_id):
    """ View to send the form to delete users.

    """
    if request.is_ajax():
        user = User.objects.get(pk=user_id)
        form = DeleteUserForm(initial={'user_id': user.pk})
        return render(request, 'administracion/user_delete_modal.html',
                      {'delete_user': user, 'delete_form': form})


@login_required
@user_passes_test(is_administrador)
def admin_users_delete(request):
    """ View to delete users.

    """
    if request.method == 'POST':
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('administracion:users')
