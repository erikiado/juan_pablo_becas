from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from perfiles_usuario.utils import is_directivo

@login_required
@user_passes_test(is_directivo)
def all_indicators(request):
    """ View to see the list of indicators for the beca calculation.

    """

    return render(request, 'indicadores/all_indicators.html')


@login_required
@user_passes_test(is_directivo)
def show_indicator(request):
    """ View to see the detail of an indicator.

    """

    return render(request, 'indicadores/indicator_detail.html')
