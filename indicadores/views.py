from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from perfiles_usuario.utils import is_directivo


@login_required
@user_passes_test(is_directivo)
def all_indicators(request):
    """ View to see the list of indicators for the beca calculation.
    TODO. This is a dummy view, therefore it may
    be changed in the future.
    """

    return render(request, 'administracion/dashboard_users.html')


@login_required
@user_passes_test(is_directivo)
def show_indicator(request):
    """ View to see the detail of an indicator.
    TODO. This is a dummy view, therefore it may
    be changed in the future.
    """

    return render(request, 'indicadores/indicator_detail.html')
