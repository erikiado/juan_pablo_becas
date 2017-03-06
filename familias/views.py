from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from perfiles_usuario.utils import is_administrador

@login_required
@user_passes_test(is_administrador)
def families_directory(request):
    """ View to show all the families and their members.

    """

    return render(request, 'familias/all_families.html')


@login_required
@user_passes_test(is_administrador)
def family_member(request):
    """ View to show the detail of a family member.

    """

    return render(request, 'familias/family_member.html')
