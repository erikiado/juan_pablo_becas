from django import forms


class BecaForm(forms.Form):
    """ This form is used to assign a scolarship
    to a set of students. It just has an option for
    the tabulador used, and a list of possible percentages
    of scolarship.
    """
    CATORCE = '14_percent'
    VEINTE = '20_percent'
    OPCIONES_TABULADOR = (
        (CATORCE, 'Asignar 14%'),
        (VEINTE, 'Asignar 20%')
    )

    OPCIONES_PORCENTAJE = [
        (x, x + '%') for x in map(lambda x: str(x), range(1, 101))
    ]

    tabulador = forms.ChoiceField(choices=OPCIONES_TABULADOR,
                                  required=True)

    porcentaje = forms.ChoiceField(choices=OPCIONES_PORCENTAJE)

    def __init__(self, *args, **kwargs):
        # Add the class form-control to all of the fields
        super(BecaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
