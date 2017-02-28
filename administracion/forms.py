from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, DIRECTIVO_GROUP, \
                                   SERVICIOS_ESCOLARES_GROUP
from perfiles_usuario.models import Capturista


class UserModelForm(forms.ModelForm):
    """ ModelForm for Users.

    This is the general model form for creating users.
    """

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': ('Nombre de Usuario'),
            'first_name': ('Nombre'),
            'last_name': ('Apellido'),
            'email': ('Email')
        }


class UserForm(UserModelForm):
    """ Form for creating and updating different types of users.

    This form inherits from UserModelForm, and is meant to be used for
    the creation of any kind of user by the administrative.

    The save method is overriden to add the corresponding group to the created user.
    """
    ROLES_USUARIO = (
        (ADMINISTRADOR_GROUP, (ADMINISTRADOR_GROUP)),
        (CAPTURISTA_GROUP, (CAPTURISTA_GROUP)),
        (DIRECTIVO_GROUP, (DIRECTIVO_GROUP)),
        (SERVICIOS_ESCOLARES_GROUP, (SERVICIOS_ESCOLARES_GROUP))
    )

    rol_usuario = forms.ChoiceField(choices=ROLES_USUARIO, label='Tipo de usuario', required=True)

    def generate_user_password(self):
        return self.instance.first_name+'_'+self.instance.last_name

    def save(self, *args, **kwargs):
        """ Override save method to add group to the user.

        This overrides the save method of forms.ModelForm so that we can
        add the corresponding group to the user that is being created.
        The group is chosen based on the ChoiceField defined above
        """
        data = self.cleaned_data
        # Create user
        if self.instance.pk is None:
            user = super(UserForm, self).save(*args, **kwargs)
            # TODO: Change the password generation for an PasswordResetForm
            user.set_password(self.generate_user_password())
            if data['rol_usuario'] == CAPTURISTA_GROUP:
                user.save()
                # capturista's group is added in the save method of the Model.
                capturista = Capturista(user=user)
                capturista.save()
            else:
                user_group = Group.objects.get_or_create(name=data['rol_usuario'])[0]
                user.groups.add(user_group)
                user.save()

        # Update user
        else:
            user = self.instance
            user.username = data['username']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']

            user_group_name = user.groups.all()[0].name

            if data['rol_usuario'] != user_group_name:
                user.groups.clear()
                if data['rol_usuario'] == CAPTURISTA_GROUP:
                    user.save()
                    capturista = Capturista(user=user)
                    capturista.save()
                else:
                    if user_group_name == CAPTURISTA_GROUP:
                        capturista = Capturista.objects.get(user=user)
                        capturista.delete()
                    user_group = Group.objects.get_or_create(name=data['rol_usuario'])[0]
                    user.groups.add(user_group)
                    user.save()
            else:
                user.save()
        return user

class UserUpdateForm(FormaCreacionUsuario):
    """ Form for creating different types of users.

    This form inherits from FormaUsuario, and is meant to be used for
    the creation of any kind of user by the administrative.

    The save method is overriden to add the corresponding group to the created user.
    """


    # def __init__(self, *args, **kwargs):

        # initial =  kwargs.get('initial', {})
        # rol_usuario = initial.get('rol_usuario', None)

        # set just the initial value
        # in the real form needs something like this {'choice':'a'}
        # but in this case you want {'choice':('a', 'letter_a')}
        # if rol_usuario:
            # kwargs['initial']['rol_usuario'] = kwargs['instance'].groups.all()[0]
        # super(UserUpdateForm, self).__init__(*args, **kwargs)
        # print(kwargs['instance'].groups.all()[0].name)

        # self.fields['rol_usuario'] = kwargs['instance'].groups.all()[0].name

    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta(FormaUsuario.Meta):
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, *args, **kwargs):
        """ Override save method to add group to the user.

        This overrides the save method of forms.ModelForm so that we can
        add the corresponding group to the user that is being created.
        The group is chosen based on the ChoiceField defined above
        """
        user = super(FormaCreacionUsuario, self).save(*args, **kwargs)
        data = self.cleaned_data
        # print(data)
        # print(user)
        if user.groups.all()[0].name == CAPTURISTA_GROUP:
            print(user)
        else:
            print("NEL")

        # if data['rol_usuario'] == CAPTURISTA_GROUP:
        #     # capturista's group is added in the save method of the Model.
        #     capturista = Capturista(user=user)
        #     capturista.save()
        # else:
        #     user_group = Group.objects.get_or_create(name=data['rol_usuario'])[0]
        #     user.groups.add(user_group)
        #     user.save()
        return user
