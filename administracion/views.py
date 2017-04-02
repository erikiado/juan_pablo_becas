from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required

from .forms import UserForm, DeleteUserForm, FeedbackForm
from perfiles_usuario.utils import is_administrador
from estudios_socioeconomicos.models import Estudio
from familias.models import Alumno


@login_required
@user_passes_test(is_administrador)
def admin_main_dashboard(request):
    """View to render the main control dashboard.

    """
    return render(request, 'administracion/dashboard_main.html',
                  {'status_options': Estudio.get_options_status()})


@login_required
@user_passes_test(is_administrador)
def admin_users_dashboard(request):
    """View to render the users control dashboard.

    """
    users = User.objects.all()
    create_user_form = UserForm()

    return render(request, 'administracion/dashboard_users.html',
                  {'all_users': users,
                   'create_user_form': create_user_form,
                   'status_options': Estudio.get_options_status()})


@login_required
@user_passes_test(is_administrador)
def admin_users_create(request):
    """ View to create users.

    """
    if request.method == 'POST':
        # kwargs = {'request': request}
        forma = UserForm(request.POST)
        if forma.is_valid():
            forma.save(request=request)
            return redirect('administracion:users')


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


@login_required
@user_passes_test(is_administrador)
def list_studies(request, status_study):
    """ View to list the studies with a specific status according to the button pushed

    """
    estudios = Estudio.objects.filter(status=status_study)
    contexto = {'estudios': estudios, 'estado': status_study,
                'status_options': Estudio.get_options_status()}
    return render(request, 'estudios_socioeconomicos/principal.html', contexto)


@login_required
@user_passes_test(is_administrador)
def focus_mode(request, study_id):
    """ View to show the detail of a study.

    TODO: This should be filled with all the info of the study.
    """
    context = {'status_options': Estudio.get_options_status()}
    estudio = Estudio.objects.get(pk=study_id)
    if estudio.status == Estudio.REVISION:
        feedback_form = FeedbackForm(initial={'estudio': estudio,
                                              'usuario': request.user})
        context['feedback_form'] = feedback_form
    return render(request, 'administracion/focus_mode.html', context)


@login_required
@user_passes_test(is_administrador)
def reject_study(request):
    """ View to reject a study.

    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('administracion:main_estudios', Estudio.RECHAZADO)


@login_required
@user_passes_test(is_administrador)
def search_students(request):
    """ View to list all active students.

    """
    students = Alumno.objects.filter(activo=True)
    return render(request, 'administracion/search_students.html', {'students': students})
