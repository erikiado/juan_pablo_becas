from django.forms import ModelForm, ChoiceField, HiddenInput, ModelChoiceField, CharField, \
                         ValidationError, Form, IntegerField
from administracion.models import Escuela
from .models import Familia, Integrante, Alumno, Tutor


class FamiliaForm(ModelForm):
    """ Model form for familia

        This is the general form for updating a Familia.
    """
    class Meta:
        model = Familia
        fields = ('nombre_familiar',
                  'numero_hijos_diferentes_papas',
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
    OPCION_ROL_HERMANO = 'hermano'
    OPCION_ROL_ABUELO = 'abuelo'
    OPCION_ROL_TIO = 'tio'
    OPCIONES_ROL = ((OPCION_ROL_NINGUNO, 'Ninguno'),
                    (OPCION_ROL_TUTOR, 'Tutor'),
                    (OPCION_ROL_ALUMNO, 'Alumno'),
                    (OPCION_ROL_HERMANO, 'Hermano/a'),
                    (OPCION_ROL_ABUELO, 'Abuelo/a'),
                    (OPCION_ROL_TIO, 'Tío/a'))

    rol = ChoiceField(choices=OPCIONES_ROL, required=False)

    class Meta:
        model = Integrante
        fields = ('rol',
                  'familia',
                  'nombres',
                  'apellidos',
                  'oficio',
                  'telefono',
                  'correo',
                  'nivel_estudios',
                  'fecha_de_nacimiento',
                  'sacramentos_faltantes',
                  'historial_terapia')
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
    It inherits from the regular model form IntegranteForm and adds
    the extra fields needed for alumnos and tutors.
    """
    # deep copy adding the no relation option.
    OPCIONES_RELACION = (('', '---------'),) + Tutor.OPCIONES_RELACION
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
        has the necessary fields in the cleaned_data.
        """
        cleaned_data = super(IntegranteModelForm, self).clean()

        if cleaned_data['rol'] == IntegranteForm.OPCION_ROL_ALUMNO:
            if not cleaned_data['numero_sae'] or not cleaned_data['escuela']:
                raise ValidationError('El estudiante necesita el número sae y la escuela')
            if cleaned_data['relacion']:
                raise ValidationError('El estudiante no tiene relación')
            return cleaned_data

        if cleaned_data['rol'] == IntegranteForm.OPCION_ROL_TUTOR:
            if not cleaned_data['relacion']:
                raise ValidationError('El tutor necesita un tipo de relación')
            if cleaned_data['numero_sae'] or cleaned_data['escuela']:
                raise ValidationError('El tutor no tiene número sae ni escuela')
            return cleaned_data

        if cleaned_data['rol'] != IntegranteForm.OPCION_ROL_ALUMNO and \
           cleaned_data['rol'] != IntegranteForm.OPCION_ROL_TUTOR:
            if cleaned_data['numero_sae'] or cleaned_data['escuela'] or cleaned_data['relacion']:
                raise ValidationError('El integrante no tiene número sae, escuela o relación')
            return cleaned_data
        raise ValidationError('Rol inválido')

    def save(self, request=None, *args, **kwargs):
        """ Override save to create/edit the Integrante, Alumno, and Tutor.

        BEWARE: This currently does not work if when editing, we change the role of a
        integrante.
        """
        if self.instance.pk is None:   # create integrante
            integrante = super(IntegranteModelForm, self).save(*args, **kwargs)
            data = self.cleaned_data
            if data['rol'] == IntegranteForm.OPCION_ROL_TUTOR:
                Tutor.objects.create(integrante=integrante, relacion=data['relacion'])
            elif data['rol'] == IntegranteForm.OPCION_ROL_ALUMNO:
                Alumno.objects.create(integrante=integrante, numero_sae=data['numero_sae'],
                                      escuela=data['escuela'])
            return integrante
        else:  # edit integrante
            integrante = self.instance
            data = self.cleaned_data
            # filter fields which belong to integrante and are in cleaned_data.
            for field in filter(lambda x: x in data, Integrante._meta.get_fields()):
                integrante[field.name] = data[field.name]
            integrante.save()

            if data['rol'] == IntegranteForm.OPCION_ROL_TUTOR:
                tutor = Tutor.objects.get(integrante=integrante)
                tutor.relacion = data['relacion']
                tutor.save()
            elif data['rol'] == IntegranteForm.OPCION_ROL_ALUMNO:
                alumno = Alumno.objects.get(integrante=integrante)
                alumno.numero_sae = data['numero_sae']
                alumno.escuela = data['escuela']
                alumno.save()
            return Integrante.objects.get(pk=self.instance.pk)


class DeleteIntegranteForm(Form):
    """Form to delete user from dashboard which is used to validate the post information.

    """
    id_integrante = IntegerField(widget=HiddenInput())

    def clean(self):
        """ Override clean data to validate the id corresponds
        to a real integrante.
        """
        cleaned_data = super(DeleteIntegranteForm, self).clean()
        integrante = Integrante.objects.filter(pk=cleaned_data['id_integrante'])
        if not integrante:
            raise ValidationError('El integrante no existe')
        return cleaned_data

    def save(self, *args, **kwargs):
        """ Override save to soft delete the integrante.
        We also take care of the case in which there's
        an alumno related to it.
        """
        integrante = Integrante.objects.get(pk=self.cleaned_data['id_integrante'])
        integrante.activo = False
        if hasattr(integrante, 'alumno_integrante'):
            integrante.alumno_integrante.activo = False
            integrante.alumno_integrante.save()
        integrante.save()
