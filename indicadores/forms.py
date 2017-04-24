from django.forms import Form, ModelForm, HiddenInput, IntegerField, ValidationError
from familias.models import Integrante, Tutor
from .models import Transaccion, Ingreso


class TransaccionForm(ModelForm):
    """ Model form for Transaccion

    This is the general form for updating and creating a
    transaccion.
    """

    id_transaccion = IntegerField(required=False, widget=HiddenInput())

    class Meta:
        model = Transaccion
        fields = ('monto',
                  'periodicidad',
                  'observacion',
                  'es_ingreso',
                  'familia')
        widgets = {
            'es_ingreso': HiddenInput(),
            'familia': HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        # Add the class form-control to all of the fields
        super(TransaccionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class IngresoForm(ModelForm):
    """ Model form for Ingreso

    This is the general form for creating and updating an
    ingreso.
    """

    class Meta:
        model = Ingreso
        fields = ('fecha',
                  'tipo',
                  'tutor')
        labels = {
            'fecha': '¿Desde cuándo recibe el ingreso?'
        }

    def __init__(self, id_familia, *args, **kwargs):
        # Add the class form-control to all of the fields
        super(IngresoForm, self).__init__(*args, **kwargs)
        # Get only the tutores that are part of the family.
        integrantes = Integrante.objects.filter(familia=id_familia).values_list('id', flat=True)
        tutores = Tutor.objects.filter(integrante__in=integrantes)
        self.fields['tutor'].queryset = tutores
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class DeleteTransaccionForm(Form):
    """Form to delete user from dashboard which is used to validate the post information.

    """
    id_transaccion = IntegerField(widget=HiddenInput())

    def clean(self):
        """ Override clean data to validate the id corresponds
        to a real transaccion.
        """
        self.cleaned_data = super(DeleteTransaccionForm, self).clean()
        transaccion = Transaccion.objects.filter(pk=self.cleaned_data['id_transaccion'])
        if not transaccion:
            raise ValidationError('La transacción no existe')
        return self.cleaned_data

    def save(self, *args, **kwargs):
        """ Override save to soft delete the transaccion.

        """
        transaccion = Transaccion.objects.get(pk=self.cleaned_data['id_transaccion'])
        transaccion.activo = False
        transaccion.save()
