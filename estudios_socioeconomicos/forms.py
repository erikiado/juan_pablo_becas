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


class DeleteEstudioCapturistaForm(forms.Form):
    """ This form is meant to be used by Capturistas, to delete studies.

    """
    id_estudio = forms.IntegerField(widget=forms.HiddenInput())

    def save(self, *args, **kwargs):
        """Override save method to soft delete estudio instance, and related models.
        """
        data = self.cleaned_data
        estudio_instance = get_object_or_404(Estudio, pk=data['id_estudio'])
        estudio_instance.status = Estudio.ELIMINADO_CAPTURISTA
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


class RecoverEstudioForm(forms.Form):
    """ Form to recover a study that has been deleted.

    """
    id_estudio = forms.IntegerField(widget=forms.HiddenInput())

    def clean(self):
        """ Override clean data to validate the id corresponds
        to a real estudio
        """
        cleaned_data = super(RecoverEstudioForm, self).clean()
        estudios = Estudio.objects.filter(pk=cleaned_data['id_estudio'])
        if not estudios:
            raise forms.ValidationError('El estudio no existe')
        elif estudios[0].status not in [Estudio.ELIMINADO_CAPTURISTA, Estudio.ELIMINADO_ADMIN]:
            raise forms.ValidationError('El estudio no está eliminado')
        return cleaned_data

    def save(self, *args, **kwargs):
        """ Override save to change the status of the study.

        We change the status back to borrador and activate
        all the associated integrantes.
        """
        estudio = Estudio.objects.get(pk=self.cleaned_data['id_estudio'])
        integrantes = Integrante.objects.filter(familia=estudio.familia)
        for integrante in integrantes:
            integrante.activo = True
            if hasattr(integrante, 'alumno_integrante'):
                alumno = integrante.alumno_integrante
                alumno.activo = True
                alumno.save()
            integrante.save()

        if estudio.status == Estudio.ELIMINADO_CAPTURISTA:
            estudio.status = Estudio.BORRADOR
        else:
            estudio.status = Estudio.APROBADO
        estudio.save()
        return estudio
