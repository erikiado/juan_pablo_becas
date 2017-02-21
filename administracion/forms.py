from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, DIRECTIVO_GROUP, \
                                   SERVICIOS_ESCOLARES_GROUP
from perfiles_usuario.models import Capturista


class FormaUsuario(forms.ModelForm):
    """ ModelForm for Users.
    
    This is the general model form for creating users.
    """
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class FormaCreacionUsuario(FormaUsuario):
    """ Form for creating different types of users.

    This form inherits from FormaUsuario, and is meant to be used for
    the creation of any kind of user by the administrative.

    The save method is overriden to add the corresponding group to the created user.
    """
    ROLES_USUARIO = (
        (ADMINISTRADOR_GROUP, ('Administrador')),
        (CAPTURISTA_GROUP, ('Capturista')),
        (DIRECTIVO_GROUP, ('Directivo')),
        (SERVICIOS_ESCOLARES_GROUP, ('Servicios Escolares'))
    )

    rol_usuario = forms.ChoiceField(choices=ROLES_USUARIO, label='Tipo de usuario', required=True)

    def save(self, *args, **kwargs):
        """ Override save method to add group to the user.

        This overrides the save method of forms.ModelForm so that we can
        add the corresponding group to the user that is being created.
        The group is chosen based on the ChoiceField defined above
        """
        user = super(FormaCreacionUsuario, self).save(*args, **kwargs)
        data = self.cleaned_data
        if data['rol_usuario'] == CAPTURISTA_GROUP:
            # capturista's group is added in the save method of the Model
            capturista = Capturista(user=user)
            capturista.save()
        else:
            user_group = Group.objects.get_or_create(name=data['rol_usuario'])[0]
            user.groups.add(user_group)
            user.save()
        return user
