from django.forms import ModelForm, ChoiceField, HiddenInput, ModelChoiceField, CharField, \
                         ValidationError
from administracion.models import Escuela
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
        fields = ('familia',
                  'nombres',
                  'apellidos',
                  'telefono',
                  'correo',
                  'nivel_estudios',
                  'fecha_de_nacimiento')
        widgets = {
            'familia': HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        # This adds the class form control to every single input field.
        # Implemented for bootstrap purposes.
        super(IntegranteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class IntegranteModelForm(IntegranteForm):
    """ This is a general form for any kind of Integrante.

    Namely, this works to save and update a regular Integrante,
    a student, or a tutor.
    """
    OPCIONES_RELACION = Tutor.OPCIONES_RELACION + tuple()  # deep copy
    escuela = ModelChoiceField(required=False, queryset=Escuela.objects.all())
    numero_sae = CharField(required=False, max_length=30)
    relacion = ChoiceField(required=False, choices=OPCIONES_RELACION)

    def __init__(self, *args, **kwargs):
        # This adds the class form control to every single input field.
        # Implemented for bootstrap purposes.
        super(IntegranteModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        """ Override clean data to validate that the corresponding role
        """
        cleaned_data = super(IntegranteModelForm, self).clean()
        if cleaned_data['Rol'] == IntegranteForm.OPCION_ROL_ALUMNO:
            if not cleaned_data['numero_sae'] or not cleaned_data['escuela']:
                raise ValidationError('El estudiante necesita el número sae y la escuela')
            if cleaned_data['relacion']:
                raise ValidationError('El estudiante no tiene relación')
            return cleaned_data
        if cleaned_data['Rol'] == IntegranteForm.OPCION_ROL_TUTOR:
            if not cleaned_data['relacion']:
                raise ValidationError('El tutor necesita un tipo de relación')
            if cleaned_data['numero_sae'] or cleaned_data['escuela']:
                raise ValidationError('El tutor no tiene número sae ni escuela')
            return cleaned_data
        if cleaned_data['Rol'] == IntegranteForm.OPCION_ROL_NINGUNO:
            if cleaned_data['numero_sae'] or cleaned_data['escuela'] or cleaned_data['relacion']:
                raise ValidationError('El integrante no tiene número sae, escuela o relación')
            return cleaned_data
        raise ValidationError('Rol inválido')

    def save(self, request=None, *args, **kwargs):
        if self.instance.pk is None:
            integrante = super(IntegranteModelForm, self).save(*args, **kwargs)
            data = self.cleaned_data
            if data['Rol'] == IntegranteForm.OPCION_ROL_TUTOR:
                Tutor.objects.create(integrante=integrante, relacion=data['relacion'])
            elif data['Rol'] == IntegranteForm.OPCION_ROL_ALUMNO:
                Alumno.objects.create(integrante=integrante, numero_sae=data['numero_sae'],
                                      escuela=data['escuela'])
            return integrante


class AlumnoForm(ModelForm):
    """ Model form for Alumno

        This is the general form for updating a Alumno.
    """
    class Meta:
        model = Alumno
        fields = ('integrante',
                  'numero_sae',
                  'escuela')
        widgets = {
            'integrante': HiddenInput()
        }

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
        fields = ('integrante', 'relacion')
        widgets = {
            'integrante': HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        # This adds the class form control to every single input field.
        # Implemented for bootstrap purposes.
        super(TutorForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
