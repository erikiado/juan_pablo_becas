from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse

from perfiles_usuario.utils import is_administrador
from estudios_socioeconomicos.models import Estudio
from familias.models import Alumno
from becas.models import Beca
from becas.forms import CartaForm
from becas.utils import generate_letter
from .forms import UserForm, DeleteUserForm, FeedbackForm


@login_required
@user_passes_test(is_administrador)
def admin_users_dashboard(request):
    """View to render the users control dashboard.

    """
    users = User.objects.all()
    create_user_form = UserForm()

    return render(request, 'administracion/crud_users.html',
                  {'all_users': users,
                   'create_user_form': create_user_form})


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
    return render(request, 'estudios_socioeconomicos/listado_estudios.html', contexto)


@login_required
@user_passes_test(is_administrador)
def focus_mode(request, study_id):
    """ View to show the detail of a study.

    TODO: This should be filled with all the info of the study.
    """
    context = {}
    estudio = Estudio.objects.get(pk=study_id)
    if estudio.status == Estudio.REVISION:
        feedback_form = FeedbackForm(initial={'estudio': estudio,
                                              'usuario': request.user})
        context['feedback_form'] = feedback_form
    return render(request, 'administracion/focus_mode.html', context)


@login_required
@user_passes_test(is_administrador)
def search_students(request):
    """ View to list all active students.

    """
    students = Alumno.objects.filter(activo=True)
    return render(request, 'administracion/search_students.html', {'students': students})


@login_required
@user_passes_test(is_administrador)
def detail_student(request, id_alumno):
    """ View to show the complete information of a student, and to
    generate the letter of scholarship in case of POST.

    GET: return information of student and form to generate letter
    POST: validate information in form and return pdf
    """
    alumno = get_object_or_404(Alumno, pk=id_alumno, activo=True)
    becas = Beca.objects.filter(alumno=alumno).order_by('-fecha_de_asignacion')
    context = {
        'student': alumno,
        'becas': becas
    }
    if request.method == 'GET':
        context['form'] = CartaForm()
    else:
        form = CartaForm(request.POST)
        if form.is_valid():
            response = HttpResponse(content_type='application/pdf')
            filename = 'carta_beca_{}.pdf'.format(alumno)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
            # obtain last scholarship
            beca_actual = Beca.objects.filter(alumno=alumno).order_by('-fecha_de_asignacion')[0]

            generate_letter(response, nombre=str(alumno.integrante),
                            ciclo=form.cleaned_data['ciclo'],
                            grado=form.cleaned_data['grado'],
                            porcentaje=str(beca_actual),
                            compromiso=form.cleaned_data['compromiso'],
                            a_partir=form.cleaned_data['a_partir'])
            return response
        else:
            context['form'] = form
    return render(request, 'administracion/detail_student.html', context)
