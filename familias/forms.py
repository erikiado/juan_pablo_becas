from django.forms import ModelForm, ChoiceField
from .models import Familia, Integrante, Alumno, Tutor


class FamiliaForm(ModelForm):
    class Meta:
        model = Familia
        fields = ('numero_hijos_diferentes_papas',
                  'estado_civil',
                  'localidad')

    def __init__(self, *args, **kwargs):
        super(FamiliaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class IntegranteForm(ModelForm):
    OPCION_ROL_NINGUNO = 'Ninguno'
    OPCION_ROL_TUTOR = 'Tutor'
    OPCION_ROL_ALUMNO = 'Alumno'
    OPCIONES_ROL = ((OPCION_ROL_NINGUNO, 'Ninguno'),
                    (OPCION_ROL_TUTOR, 'Tutor'),
                    (OPCION_ROL_ALUMNO, 'Alumno'))

    Rol = ChoiceField(choices=OPCIONES_ROL, required=False)

    class Meta:
        model = Integrante
        exclude = ['familia']

    def __init__(self, *args, **kwargs):
        super(IntegranteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class AlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        exclude = ['integrante', 'activo']

    def __init__(self, *args, **kwargs):
        super(AlumnoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class TutorForm(ModelForm):
    class Meta:
        model = Tutor
        exclude = ['integrante']

    def __init__(self, *args, **kwargs):
        super(TutorForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
