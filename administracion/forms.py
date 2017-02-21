from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, DIRECTIVO_GROUP, \
                                   SERVICIOS_ESCOLARES_GROUP
from perfiles_usuario.models import Capturista


class FormaUsuario(forms.ModelForm):
    ROLES_USUARIO = (
        (ADMINISTRADOR_GROUP, ('Administrador')),
        (CAPTURISTA_GROUP, ('Capturista')),
        (DIRECTIVO_GROUP, ('Directivo')),
        (SERVICIOS_ESCOLARES_GROUP, ('Servicios Escolares'))
    )

    rol_usuario = forms.ChoiceField(choices=ROLES_USUARIO, label='Tipo de usuario', required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        user = get_user_model()(
                    username=data['username'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    password=data['password'])
        user.save()
        if data['rol_usuario'] == CAPTURISTA_GROUP:
            capturista = Capturista(user=user)
            capturista.save()
        else:
            user_group = Group.objects.get_or_create(name=data['rol_usuario'])[0]
            user.groups.add(user_group)
            user.save()
        return user
