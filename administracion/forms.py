from django import forms
from django.contrib.auth import get_user_model


class FormaUsuario(forms.ModelForm):
    ROLES_USUARIO = (
        (1, ('Administrador')),
        (2, ('Capturista')),
        (3, ('Directivo')),
        (4, ('Servicios Escolares'))
    )
    # first_name = forms.CharField(max_length=35, label='Nombre', required=True)
    # last_name = forms.CharField(max_length=35, label='Apellido', required=True)
    # email = forms.EmailField(label='Correo Electronico', required=True)
    rol_usuario = forms.ChoiceField(choice=ROLES_USUARIO, label='Tipo de usuario', required=True)
    # password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=True)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password')

    def save(self, commit=True, *args, **kwargs):
        nuevo_usuario = super(FormaUsuario, self).save(commit=False, *args, **kwargs)
        nuevo_usuario.first_name = self.first_name
        nuevo_usuario.last_name = self.last_name
        nuevo_usuario.email = self.email
        nuevo_usuario.rol_usuario = self.rol_usuario
        nuevo_usuario.password = self.password
        if commit:
            nuevo_usuario.save()
        return nuevo_usuario