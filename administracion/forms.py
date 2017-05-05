from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator

from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, DIRECTIVO_GROUP, \
                                   SERVICIOS_ESCOLARES_GROUP
from perfiles_usuario.models import Capturista
from captura.models import Retroalimentacion
from estudios_socioeconomicos.models import Estudio


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

    def save(self, request=None, *args, **kwargs):
        """ Override save method to add group to the user.

        This overrides the save method of forms.ModelForm so that we can
        add the corresponding group to the user that is being created.
        The group is chosen based on the ChoiceField defined above
        """
        data = self.cleaned_data
        # Create user
        if self.instance.pk is None:
            user = super(UserForm, self).save(*args, **kwargs)
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

            # Send password reset form to new user email
            reset_form = PasswordResetForm({'email': data['email']})
            if reset_form.is_valid():
                opts = {
                    'request': request,
                    'html_email_template_name': 'registration/password_reset_email.html',
                    'email_template_name': 'registration/password_reset_email.html',
                    'subject_template_name': 'registration/password_reset_subject.txt',
                    'use_https': request.is_secure(),
                    'token_generator': default_token_generator,
                    'extra_email_context': None,
                }
                reset_form.save(**opts)

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


class DeleteUserForm(forms.Form):
    """Form to delete user from dashboard which is used to validate the post information.

    """
    user_id = forms.IntegerField(widget=forms.HiddenInput())

    def save(self, *args, **kwargs):
        """Override save method to delete user instance.

        """
        data = self.cleaned_data
        user_instance = User.objects.get(pk=data['user_id'])
        user_instance.delete()


class FeedbackForm(forms.ModelForm):
    """ Form to save the feedback given on a study.

    Note that we expect the study and user pre-filled when
    creating this form.
    """
    class Meta:
        model = Retroalimentacion
        fields = ['estudio', 'usuario', 'descripcion']

        widgets = {
            'estudio': forms.HiddenInput(),
            'usuario': forms.HiddenInput(),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, *args, **kwargs):
        """ Change the status of the study after submiting
        the feedback.

        If the study was under revision from the admin, it goes to
        rejected. Conversely, it can go from rejected to revision.
        """
        feedback = super(FeedbackForm, self).save(*args, **kwargs)
        estudio = feedback.estudio
        if estudio.status == Estudio.REVISION:
            estudio.status = Estudio.RECHAZADO
        elif estudio.status == Estudio.RECHAZADO:
            estudio.status = Estudio.REVISION
        estudio.save()
        return feedback
