from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from perfiles_usuario.utils import is_capturista


@login_required
@user_passes_test(is_capturista)
def pending_studies(request):
    """ View to see the list of pending studies.
    TODO. This is a dummy view, therefore it may
    be changed in the future.

    """

    return render(request, 'administracion/dashboard_users.html')


@login_required
@user_passes_test(is_capturista)
def show_family(request):
    """ View to see the members of the family of a certain study.
    TODO. This is a dummy view, therefore it may
    be changed in the future.
    """

    return render(request, 'captura/family.html')


@login_required
@user_passes_test(is_capturista)
def show_economy(request):
    """ View to see the ingresos and egresos of the family.
    TODO. This is a dummy view, therefore it may
    be changed in the future.
    """

    return render(request, 'captura/economy.html')


@login_required
@user_passes_test(is_capturista)
def show_housing(request):
    """ View to see data about the vivienda of the family.
    TODO. This is a dummy view, therefore it may
    be changed in the future.
    """

    return render(request, 'captura/housing.html')


@login_required
@user_passes_test(is_capturista)
def cycle_sections(request):
    """ View to cycle through the sections above.
    TODO. This is a dummy view, therefore it may
    be changed in the future.
    """

    return render(request, 'captura/sections.html')
