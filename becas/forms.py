from django import forms
from .utils import PORCENTAJE_A_MONTO


class BecaForm(forms.Form):
    CATORCE = '14_percent'
    VEINTE = '20_percent'
    OPCIONES_TABULADOR = (
        (CATORCE, 'Asignar 14%'),
        (VEINTE, 'Asignar 20%')
    )

    OPCIONES_PORCENTAJE = [
        (x, x) for x in sorted(PORCENTAJE_A_MONTO.keys(), key=lambda x: int(x[:-1]))
    ]

    tabulador = forms.ChoiceField(choices=OPCIONES_TABULADOR,
                                  required=True)

    porcentaje = forms.ChoiceField(choices=OPCIONES_PORCENTAJE)

    def __init__(self, *args, **kwargs):
        # Add the class form-control to all of the fields
        super(BecaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
