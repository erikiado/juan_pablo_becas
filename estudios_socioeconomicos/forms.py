from django import forms

from .models import Respuesta, OpcionRespuesta


class RespuestaForm(forms.ModelForm):
    """ Model form for answers

        This is the general form for saving an answer.
    """

    def __init__(self, *args, **kwargs):
        """
        """
        pregunta = kwargs.pop('pregunta', None)
        super(RespuestaForm, self).__init__(*args, **kwargs)
        if pregunta:
            self.fields['elecciones'].queryset = OpcionRespuesta.objects.filter(pregunta=pregunta)
       
        if 'instance' in kwargs:
            self.fields['elecciones'].initial = self.instance.elecciones

    respuesta = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    elecciones = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        queryset=[])

    
    def save(self, commit=True, *args, **kwargs):

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
        fields = ('respuesta','elecciones')
        exclude = ('pregunta', 'integrante')
