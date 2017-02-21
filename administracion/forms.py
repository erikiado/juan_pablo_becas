from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from perfiles_usuario.utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP, DIRECTIVO_GROUP, \
                                   SERVICIOS_ESCOLARES_GROUP

class FormaUsuario(forms.ModelForm):
    ROLES_USUARIO = (
        ('ADMINISTRADOR_GROUP', ('Administrador')),
        ('CAPTURISTA_GROUP', ('Capturista')),
        ('DIRECTIVO_GROUP', ('Directivo')),
        ('SERVICIOS_ESCOLARES_GROUP', ('Servicios Escolares'))
    )
    # first_name = forms.CharField(max_length=35, label='Nombre', required=True)
    # last_name = forms.CharField(max_length=35, label='Apellido', required=True)
    # email = forms.EmailField(label='Correo Electronico', required=True)
    rol_usuario = forms.ChoiceField(choices=ROLES_USUARIO, label='Tipo de usuario', required=True)
    # password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=True)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password')

    def save(self, commit=True, *args, **kwargs):
        # print(self)
        nuevo_usuario = super(FormaUsuario, self).save(commit=False, *args, **kwargs)
        nuevo_usuario.first_name = self.cleaned_data['first_name']
        nuevo_usuario.last_name = self.cleaned_data['last_name']
        nuevo_usuario.email = self.cleaned_data['email']
        print(self.cleaned_data['rol_usuario'])
        rol = Group.objects.get_or_create(self.cleaned_data['rol_usuario'])[0]
        nuevo_usuario.groups.add(rol)
        nuevo_usuario.password = self.cleaned_data['password']
        if commit:
            nuevo_usuario.save()
        return nuevo_usuario