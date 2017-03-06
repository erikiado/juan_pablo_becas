from django import forms

from .models import Respuesta, OpcionRespuesta


class RespuestaForm(forms.ModelForm):
    """ Model form for answers

        This is the general form for saving an answer.
    """

    def __init__(self, *args, **kwargs):
        """ Overide __init__ method to add query to elections multiple select.

            The 'elecciones' field in this form need a query set that depends
            upon the specific question insance. (Certain question have)
            predefined answer choices. This custom init recieves the instance
            of the question this RespuestaForm will be answering to query
            the options for that question.
        """
        pregunta = kwargs.pop('pregunta', None)
        super(RespuestaForm, self).__init__(*args, **kwargs)
        if pregunta:
            self.fields['elecciones'].queryset = OpcionRespuesta.objects.filter(pregunta=pregunta)

        if 'instance' in kwargs:
            self.fields['elecciones'].initial = self.instance.elecciones

    respuesta = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control answer-input'}))

    elecciones = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        queryset=[])  # Empty Queryset so questions with no options get nothing rendered.

    def save(self, commit=True, *args, **kwargs):
        """ Overwrite form save method to save the Many to Many answer - question option relashionship.
        """
        instance = super(RespuestaForm, self).save(commit=False)
        key = 'respuesta-' + str(instance.id) + '-elecciones'

        if key in self.data and self.data[key]:
            instance.elecciones.clear()
            opcion_respuesta = OpcionRespuesta.objects.get(pk=self.data[key])
            instance.elecciones.add(opcion_respuesta)

        instance.save()

        return instance

    class Meta:
        model = Respuesta
        fields = ('respuesta', 'elecciones')
        exclude = ('pregunta', 'integrante')
