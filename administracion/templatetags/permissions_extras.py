from django import template

from estudios_socioeconomicos.models import Estudio
from perfiles_usuario.utils import is_capturista, is_administrador
from captura.utils import user_can_modify_study

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """ Function to check if a user belongs to a group in a template.

        Registers a new template tag that checks a user belongs to a
        group. This is used in the sidebar to display the correctly
        section for each group.

        Django checks by default on the root of each projet for a
        folder called templatetags to add custom templatetags.
    """
    return user.groups.filter(name=group_name).exists()


@register.filter(name='can_modify_study')
def can_modify_study(user, study):
    """
    """
    return user_can_modify_study(user, study)

