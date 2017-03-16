from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from perfiles_usuario.utils import is_servicios_escolares


@login_required
@user_passes_test(is_servicios_escolares)
def reinscription_studies_left(request):
    """ View to see the list of studies that require to
    be marked for reinscription and therefore assing a new
    scolarship for the student.
    TODO. This is a dummy view, therefore it may
    be changed in the future.

    """

    return render(request, 'administracion/dashboard_users.html')
