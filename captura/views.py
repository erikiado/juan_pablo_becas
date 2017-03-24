from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import ObjectDoesNotExist
from django.forms import HiddenInput
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse

from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


from perfiles_usuario.utils import is_capturista
from perfiles_usuario.models import Capturista
from estudios_socioeconomicos.forms import RespuestaForm
from estudios_socioeconomicos.serializers import SeccionSerializer, EstudioSerializer
from estudios_socioeconomicos.models import Respuesta, Pregunta, Seccion, Estudio
from familias.forms import FamiliaForm, IntegranteForm, AlumnoForm, TutorForm
from familias.models import Familia, Integrante, Alumno, Tutor
from administracion.models import Escuela
from .utils import SECTIONS_FLOW, get_study_info_for_section


@login_required
@user_passes_test(is_capturista)
def add_answer_study(request):
    """ View to create a new answer for a specific question in an existing study.

        This view is meant to be called through AJAX while a capturista user is
        answering a study. Any given question can have multiple answers, since
        we are generating the answers with blank data before the user fills them,
        when he is answering a new study he can add as many answers as he wish to
        a question. This view recieves the id for the study and for the question,
        creates the answer question, creates a form and returns it to the user.

        Parameters
        ----------
        All parameters must go through POST method

        id_estudio : int
            The id of the study the user wishes to add an answer to.
        id_pregunta : int
            The id of the question inside the study user wishes to add answer to.

        Returns
        ----------
        returns HTTP STATUS CODE 201 on succes.
        returns HTTP STATUS CODE 404 on error.

        form : estudios_socioeconomicos.forms.RespuestaForm
            A rendered form for the created object inside a HttpResponse.

        Raises
        ----------
        HTTP STATUS 404
            If either study or question do not exist in database.

        Notes
        ----------
        is_ajax() function makes the functionality in this view
        only accessible through XMLHttpRequest.

    """
    if request.method == 'POST' and request.is_ajax():

        estudio = get_object_or_404(Estudio, pk=request.POST.get('id_estudio'))
        pregunta = get_object_or_404(Pregunta, pk=request.POST.get('id_pregunta'))

        respuesta = Respuesta.objects.create(estudio=estudio, pregunta=pregunta)

        form = RespuestaForm(
            instance=respuesta,
            pregunta=pregunta,
            prefix='respuesta-{}'.format(respuesta.id))

        return HttpResponse(form, status=status.HTTP_201_CREATED)


@login_required
@user_passes_test(is_capturista)
def remove_answer_study(request):
    """ View to delete a specific answer to a question inside a study.

        This view is meant to be called through AJAX while a capturista
        user if creating or modifying a study. Since any question can
        have multiple answers, a capturista can delete any of this answers.

        Parameters
        ----------
        All parameters must go through POST method

        id_respuesta : int
            The id of the answer the user wishes to remove.

        Returns
        ----------

        returns HTTP STATUS CODE 202 on succes.
        returns HTTP STATUS CODE 404 on error.

        Raises
        ----------
        HTTP STATUS 404
            If answer do not exist in database.

        Notes
        ----------
        is_ajax() function makes the functionality in this view
        only accessible through XMLHttpRequest.
    """
    if request.method == 'POST' and request.is_ajax():

        get_object_or_404(Respuesta, pk=request.POST.get('id_respuesta')).delete()
        return HttpResponse(status=status.HTTP_202_ACCEPTED)


@login_required
@user_passes_test(is_capturista)
def capture_study(request, id_estudio, numero_seccion):
    """ View for filling the non statistic parts of a study.

        @TODO: Currently section 5 does not exist, so I am
        hardcoding this view to jump it, this should be
        removed in the future.

        @TODO: Remove + 1 from max_number_sections when we
        add section 5. If this is removed, check utils.SECTIONS_FLOW,
        it contains the logic to map its section to its predesecor and
        succesor. Any changes in the way we store studies, should also
        change this.


        This view helps a Capturista user fill out all the information
        that will not be used for statistical indicators in a study.
        This view recieves the id of the study the capturista wants to
        fill, and the number of section inside the study.

        This function calls .utils.get_study_info_for_section, this function
        returns an object with all the information we need nested and organized.
        (subsecciones, preguntas, respuestas, opciones de respuestas) for easy
        rendering.

        On POST we iterate all saved answers and bind them back to the sent forms
        to save the edition of each object in the database.

        Returns
        ----------
        GET:
            On succes returns HTTP 200 with captura/captura_estudio.html
            template rendeered.

            On error returns HTTP 404

        POST:
            On succes returns HTTP 301 redirect to the next or previous
            section of the study.

            On error returns HTTP 404


        Raises
        ----------
        HTTP STATUS 404
            If the study or section do not exist in the database.

    """
    context = {}
    estudio = get_object_or_404(Estudio, pk=id_estudio)
    seccion = get_object_or_404(Seccion, numero=numero_seccion)

    (data, respuestas) = get_study_info_for_section(estudio, seccion)

    if request.method == 'POST':
        for respuesta in respuestas:
            form = RespuestaForm(
                request.POST,
                instance=respuesta,
                prefix='respuesta-{}'.format(respuesta.id),
                pregunta=respuesta.pregunta.id)

            if form.is_valid():
                form.save()

        next_section = SECTIONS_FLOW.get(seccion.numero).get(request.POST.get('next', ''))

        if next_section:  # if anybody messes with JS it will return None
            return redirect(
                    'captura:contestar_estudio',
                    id_estudio=id_estudio,
                    numero_seccion=next_section)

    context['max_num_sections'] = Seccion.objects.all().count() + 1  # Compensate missing section
    context['data'] = data
    context['id_estudio'] = id_estudio
    context['seccion'] = seccion
    context['status_options'] = Estudio.get_options_status()

    return render(request, 'captura/captura_estudio.html', context)


@login_required
@user_passes_test(is_capturista)
def capturista_dashboard(request):
    """View to render the capturista control dashboard.

       This view shows the list of socio-economic studies that are under review
       and the button to add a new socio-economic study.
       Also shows the edit and see feedback buttons to each socio-economic study
       shown in the list if this exists for the current user (capturist).
    """
    context = {}

    estudios = Estudio.objects.filter(
            status__in=[Estudio.RECHAZADO, Estudio.REVISION, Estudio.BORRADOR],
            capturista=Capturista.objects.get(user=request.user)).order_by('status')

    context['estudios'] = estudios
    context['status_options'] = Estudio.get_options_status()
    return render(request, 'captura/dashboard_capturista.html', context)


@login_required
@user_passes_test(is_capturista)
def create_estudio(request):
    """ This view creates the family, and estudio entities that are
    required for the creation and fullfillment of every piece of functionality
    in this app.
    """
    if request.method == 'POST':
        familia = Familia.objects.create()
        Estudio.objects.create(capturista=request.user.capturista, familia=familia)
        return redirect(reverse('captura:familia', kwargs={'id_familia': familia.id}))


@login_required
@user_passes_test(is_capturista)
def familia(request, id_familia):
    """ This view allows a capturista to capture the information related
    to a specific family.
    """
    if request.method == 'POST':
        instance = get_object_or_404(Familia, pk=id_familia)
        form = FamiliaForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse('captura:integrantes',
                                    kwargs={'id_familia': form.instance.pk}))
    else:
        familia = Familia.objects.get(pk=id_familia)
        form = FamiliaForm(instance=familia)
        form_view = 'captura/familia_form.html'
        return render(request, 'captura/captura_base.html', {'form_view': form_view,
                                                             'form': form,
                                                             'familia': familia})


@login_required
@user_passes_test(is_capturista)
def integrantes(request, id_familia):
    """ This view allows a capturista to see all the information about the
    integrantes of a specific family, they are displayed inside a table,
    and the capturista can select each of them individually.
    """
    context = {}

    integrantes = Integrante.objects.filter(familia__pk=id_familia)
    familia = Familia.objects.get(pk=id_familia)
    context['integrantes'] = integrantes
    context['familia'] = familia
    return render(request, 'captura/dashboard_integrantes.html', context)


def integrante(request, id_integrante):
    """ This view allows, the users to edit the information of a family memeber.
    """
    tutores = ['Tutor', 'Madre', 'Padre']
    if request.method == 'POST':
        instance = get_object_or_404(Integrante, pk=id_integrante)
        integrante_form = IntegranteForm(request.POST, instance=instance)
        if integrante_form.is_valid():
            integrante_form.save()
            rol = integrante_form.cleaned_data['Rol']
            if rol == 'Alumno':
                try:
                    alumno = instance.alumno
                    alumno_form = AlumnoForm(request.POST, instance=alumno)
                    if alumno_form.is_valid():
                        alumno_form.save()
                except ObjectDoesNotExist:
                    escuela = Escuela.objects.all().first()
                    Alumno.objects.create(integrante=instance, numero_sae='000', escuela=escuela)
                    return redirect(reverse('captura:integrante',
                                            kwargs={'id_integrante': id_integrante}))
            elif rol in tutores:
                try:
                    tutor = instance.tutor
                    tutor_form = TutorForm(request.POST, instance=tutor)
                    if tutor_form.is_valid():
                        tutor_form.save()
                except ObjectDoesNotExist:
                    Tutor.objects.create(relacion=integrante_form.cleaned_data['Rol'],
                                         integrante=instance)
                    return redirect(reverse('captura:integrante',
                                            kwargs={'id_integrante': id_integrante}))
            return redirect(reverse('captura:integrantes',
                                    kwargs={'id_familia': integrante_form.instance.familia.pk}))
    else:
        forms = {}
        integrante = Integrante.objects.get(pk=id_integrante)
        rol_integrante = 'Ninguno'
        rol_disabled = False
        try:
            alumno = integrante.alumno
            forms['form_alumno'] = AlumnoForm(instance=alumno)
            rol_integrante = 'Alumno'
            rol_disabled = True
        except ObjectDoesNotExist:
            pass
        try:
            tutor = integrante.tutor
            forms['form_tutor'] = TutorForm(instance=tutor)
            rol_integrante = 'Tutor'
            rol_disabled = True
        except ObjectDoesNotExist:
            pass

        forms['integrante_form'] = IntegranteForm(instance=integrante,
                                                  initial={'Rol': rol_integrante})
        if rol_disabled:
            forms['integrante_form'].fields['Rol'].widget = HiddenInput()
        form_view = 'captura/integrante_form.html'
        return render(request, 'captura/captura_base.html', {'form_view': form_view,
                                                             'forms': forms,
                                                             'integrante': integrante})


@login_required
@user_passes_test(is_capturista)
def create_integrante(request, id_familia):
    """ This view creates a new integrante with default values, and redirects the user
    to the view for editing the newly created integrante.
    """
    if request.method == 'POST':
        familia = Familia.objects.get(pk=id_familia)
        integrante = Integrante.objects.create(familia=familia)
        return redirect(reverse('captura:integrante', kwargs={'id_integrante': integrante.id}))


class APIQuestionsInformation(generics.ListAPIView):
    """ API to get all information for question, section and subsections.

        This view is a REST endpoint for the offline application to
        get all the logic for creating studies.

        Retrieves all objects from database.

        Returns
        --------

        Returns a JSON object with nested objects in this order:
        Seccion, Subseccion, Preguntas, OpcionRespuesta
    """
    serializer_class = SeccionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Seccion.objects.all()


class APIUploadRetrieveStudy(viewsets.ViewSet):
    """ Viewset for the CRUD REST operations of a Study.

        This view handles all REST operation for a Study
        to be submitted, retrieved or updated.
    """

    def list(self, request):
        """ Retrieves all Studies in a given state that belong to
            the Capturista making the Query.

            Raises
            ------
            HTTP STATUS 404
            If there are no studies for the capturista in the database.

            Returns
            -------
            Response
                Response object containing the serializer data
        """
        queryset = Estudio.objects.filter(
            status__in=[Estudio.RECHAZADO, Estudio.REVISION, Estudio.BORRADOR])
        studys = get_list_or_404(queryset, capturista=request.user.capturista)
        serializer = EstudioSerializer(studys, many=True)

        return Response(serializer.data)

    def create(self, request):
        """ Creates and saves a new Estudio object.

            If the object is not properly serializer, a JSON
            object is returned indicating format errors.

            Returns
            -------
            On Success
                Response
                    Response object containing the serializer data
            On Error
                Response
                    Response object containing the serializer errors
        """
        serializer = EstudioSerializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.create(request.user.capturista)
            return Response(EstudioSerializer(instance).data)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """ Retrieves a specific instance of a Study.

            Raises
            ------
            HTTP STATUS 404
            If the study does not exist or it does not belong to the capturista.

            Returns
            -------
            Response
                Response object containing the serializer data
        """
        queryset = Estudio.objects.filter(
            status__in=[Estudio.RECHAZADO, Estudio.REVISION, Estudio.BORRADOR],
            capturista=self.request.user.capturista)

        study = get_object_or_404(queryset, pk=pk)
        serializer = EstudioSerializer(study)

        return Response(serializer.data, status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """ Updates a specific instance of a Study.

            Raises
            ------
            HTTP STATUS 404
            If the study does not exist or it does not belong to the capturista.

            Returns
            -------
            On Success
                Response
                    Response object containing the serializer data
            On Error
                Response
                    Response object containing the serializer errors

        """
        queryset = Estudio.objects.filter(capturista=request.user.capturista)
        study = get_object_or_404(queryset, pk=pk)

        serializer = EstudioSerializer(study, data=request.data)

        if serializer.is_valid():
            update = serializer.update()
            return Response(EstudioSerializer(update).data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
