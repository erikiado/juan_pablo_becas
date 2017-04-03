from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def all_indicadores(request):
    """ DUMMY VIEW.

    This functions is currently just being used to test the redirect
    from base.

    TODO: name properly and implement everything
    """
    return render(request, 'layouts/dashboard_base.html')
