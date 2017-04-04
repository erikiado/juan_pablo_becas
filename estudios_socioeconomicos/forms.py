from django import forms
from django.shortcuts import get_object_or_404
from familias.models import Integrante, Alumno
from .models import Estudio, Respuesta, OpcionRespuesta


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
            self.fields['eleccion'].queryset = OpcionRespuesta.objects.filter(pregunta=pregunta)

        if 'instance' in kwargs:
            self.fields['eleccion'].initial = self.instance.eleccion

    respuesta = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control answer-input'}))

    eleccion = forms.ModelChoiceField(
        required=False,
        empty_label=None,
        widget=forms.RadioSelect(attrs={'class': 'form-control'}),
        queryset=[])  # Empty Queryset so questions with no options get nothing rendered.

    class Meta:
        model = Respuesta
        fields = ('respuesta', 'eleccion')

        exclude = ('pregunta', 'integrante')


class DeleteEstudioForm(forms.Form):
    """ Form to delete study from dashboard, it is used to validate the post information.

    """
    id_estudio = forms.IntegerField(widget=forms.HiddenInput())

    def save(self, *args, **kwargs):
        """Override save method to soft delete estudio instance, and related models.
        """
        data = self.cleaned_data
        estudio_instance = get_object_or_404(Estudio, pk=data['id_estudio'])
        estudio_instance.status = Estudio.ELIMINADO
        integrantes = Integrante.objects.filter(familia=estudio_instance.familia)
        for integrante in integrantes:
            integrante.activo = False
            alumnos = Alumno.objects.filter(integrante=integrante)
            if alumnos:
                alumno = alumnos[0]
                alumno.activo = False
                alumno.save()
            integrante.save()
        estudio_instance.save()
