from django import forms

from .models import Respuesta


class RespuestaForm(forms.ModelForm):
    """ Model form for answers

        This is the general form for saving an answer.
    """

    respuesta = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Respuesta
        fields = ('respuesta',)
        exclude = ('pregunta', 'integrante', 'elecciones')
