from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def all_indicadores(request):
    """ DUMMY VIEW.

    This functions is currently just being used to test the redirect
    from base.

    TODO: name properly and implement everything
    """
    return render(request, 'administracion/dashboard_users.html')


@login_required
def show_indicator(request):
    """ View to see the detail of an indicator.
    TODO. This is a dummy view, therefore it may
    be changed in the future.
    """

    return render(request, 'indicadores/indicator_detail.html')
