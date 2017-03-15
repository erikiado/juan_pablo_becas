from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


from rest_framework import status

from perfiles_usuario.utils import is_capturista
from estudios_socioeconomicos.forms import RespuestaForm
from perfiles_usuario.models import Capturista
from estudios_socioeconomicos.models import Respuesta, Pregunta, Seccion, Estudio
from familias.models import Familia
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
    estudios = Estudio.objects.filter(
            status__in=[Estudio.RECHAZADO, Estudio.REVISION, Estudio.BORRADOR],
            capturista=Capturista.objects.get(user=request.user)).order_by('status')
    return render(request, 'captura/dashboard_capturista.html',
                  {'estudios': estudios, 'Estudio': Estudio})


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
        return redirect(reverse('home'))
