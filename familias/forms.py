from django.forms import ModelForm, ChoiceField
from .models import Familia, Integrante, Alumno, Tutor


class FamiliaForm(ModelForm):
    """ Model form for familia

        This is the general form for updating a Familia.
    """
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
    """ Model form for Integrante

        This is the general form for updating a Integrante.
    """
    OPCION_ROL_NINGUNO = 'ninguno'
    OPCION_ROL_TUTOR = 'tutor'
    OPCION_ROL_ALUMNO = 'alumno'
    OPCIONES_ROL = ((OPCION_ROL_NINGUNO, 'Ninguno'),
                    (OPCION_ROL_TUTOR, 'Tutor'),
                    (OPCION_ROL_ALUMNO, 'Alumno'))

    Rol = ChoiceField(choices=OPCIONES_ROL, required=False)

    class Meta:
        model = Integrante
        fields = ('nombres',
                  'apellidos',
                  'telefono',
                  'correo',
                  'nivel_estudios',
                  'fecha_de_nacimiento')

    def __init__(self, *args, **kwargs):
        # This adds the class form control to every single input field.
        # Implemented for bootstrap purposes.
        super(IntegranteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class AlumnoForm(ModelForm):
    """ Model form for Alumno

        This is the general form for updating a Alumno.
    """
    class Meta:
        model = Alumno
        exclude = ['integrante', 'activo']

    def __init__(self, *args, **kwargs):
        # This adds the class form control to every single input field.
        # Implemented for bootstrap purposes.
        super(AlumnoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class TutorForm(ModelForm):
    """ Model form for Tutor

        This is the general form for updating a Tutor.
    """
    class Meta:
        model = Tutor
        exclude = ['integrante']

    def __init__(self, *args, **kwargs):
        # This adds the class form control to every single input field.
        # Implemented for bootstrap purposes.
        super(TutorForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
