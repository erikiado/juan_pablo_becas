""" Utility functions and constants that will be used in the project.
"""

# Names of groups for users
ADMINISTRADOR_GROUP = 'Administrador'
CAPTURISTA_GROUP = 'Capturista'
DIRECTIVO_GROUP = 'Directivo'
SERVICIOS_ESCOLARES_GROUP = 'Servicios Escolares'


def is_member(user, groups):
    """ Test if a user belongs to any of the groups provided.

    This function is meant to be used by the user_passes_test decorator to control access
    to views.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user which we are trying to identify that belongs to a certain group.
    groups : list of str
        A list of the groups we are checking if the user belongs to.

    Returns
    ---------
    bool
        True if the user belongs to any of the groups. False otherwise
    """
    return any(map(lambda g: user.groups.filter(name=g).exists(), groups))


def is_capturista_or_administrador(user):
    """ Test if a user has the administrador or capturista group.

    This function is meant to be used by the user_passes_test decorator to control access
    to views. It uses the is_member function with a predefined list of groups.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user which we are trying to identify that belongs to administrador.

    Returns
    ---------
    bool
        True if the user has administrador or capturista as a group.
    """
    return is_member(user, [ADMINISTRADOR_GROUP, CAPTURISTA_GROUP])


def is_administrador(user):
    """ Test if a user has the administrador group.

    This function is meant to be used by the user_passes_test decorator to control access
    to views. It uses the is_member function with a predefined list of groups.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user which we are trying to identify that belongs to administrador.

    Returns
    ---------
    bool
        True if the user has administrador as a group
    """
    return is_member(user, [ADMINISTRADOR_GROUP])


def is_capturista(user):
    """ Test if a user has the capturista group.

    This function is meant to be used by the user_passes_test decorator to control access
    to views. It uses the is_member function with a predefined list of groups.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user which we are trying to identify that belongs to capturista.

    Returns
    ---------
    bool
        True if the user has capturista as a group.
    """
    return is_member(user, [CAPTURISTA_GROUP])


def is_directivo(user):
    """ Test if a user has the directivo group.

    This function is meant to be used by the user_passes_test decorator to control access
    to views. It uses the is_member function with a predefined list of groups.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user which we are trying to identify that belongs to directivo.

    Returns
    ---------
    bool
        True if the user has directivo as a group.
    """
    return is_member(user, [DIRECTIVO_GROUP])


def is_servicios_escolares(user):
    """ Test if a user has the servicios_escolares group.

    This function is meant to be used by the user_passes_test decorator to control access
    to views. It uses the is_member function with a predefined list of groups.

    Parameters
    ----------
    user : django.contrib.auth.models.User
        The user which we are trying to identify that belongs to servicios_escolares.

    Returns
    ---------
    bool
        True if the user has servicios_escolares as a group.
    """
    return is_member(user, [SERVICIOS_ESCOLARES_GROUP])
