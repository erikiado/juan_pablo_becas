from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required

from rest_framework import status

from perfiles_usuario.utils import is_capturista
from estudios_socioeconomicos.forms import RespuestaForm
from estudios_socioeconomicos.models import Respuesta, Pregunta, Seccion, Subseccion, Estudio, OpcionRespuesta


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

    """
    if request.method == 'POST':
        estudio = get_object_or_404(Estudio, pk=request.POST.get('id_estudio'))
        pregunta = get_object_or_404(Pregunta, pk=request.POST.get('id_pregunta'))

        respuesta = Respuesta.objects.create(estudio=estudio, pregunta=pregunta)
        respuesta.save()
        form = RespuestaForm(instance=respuesta, pregunta=pregunta, prefix='respuesta-{}'.format(respuesta.id))

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
    """
    if request.method == 'POST':
        get_object_or_404(Respuesta, pk=request.POST.get('id_respuesta')).delete()
        return HttpResponse(status=status.HTTP_202_ACCEPTED)


@login_required
@user_passes_test(is_capturista)
def capture_study(request, id_estudio, numero_seccion):
    """ View for filling the non statistic parts of a study.

        This view helps a Capturista user fill out all the information
        that will not be used for statistical indicators in a study.
        This view recieves the id of the study the capturista wants to
        fill, and the number of section inside the study.

        For each section, we query all subsections that branch out and
        for each subsection we query all the questions that branch out.
        After that, for each question we query all the answers that have
        been created (When a study is generated a trigger automatically
        generates an empty answer for each question).  Finally we create
        a form for each answer and send the complete object of rendering.

        When we recieve a post request, we perform the same query, once
        we have all the questions, we get the form from the post data,
        bind it back to the object and save changes. 
    
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

    subsecciones = Subseccion.objects.filter(seccion=seccion).order_by('numero').values()

    for subseccion in subsecciones:
        preguntas = Pregunta.objects.filter(subseccion=subseccion['id']).order_by('orden').values()

        for pregunta in preguntas:

            respuestas = Respuesta.objects.filter(
                pregunta=pregunta['id'],
                estudio=estudio).values()

            opciones_respuesta = OpcionRespuesta.objects.filter(pregunta=pregunta['id'])

            for respuesta in respuestas:
                respuesta_obj = Respuesta.objects.get(pk=respuesta['id'])


                if request.method == 'POST':  # Bind each form to its original object
                    form = RespuestaForm(
                        request.POST,
                        instance=respuesta_obj,
                        prefix='respuesta-{}'.format(respuesta_obj.id),
                        pregunta=pregunta['id'])

                    if form.is_valid():
                        form.save()

                respuesta['form'] = RespuestaForm(
                    instance=respuesta_obj,  # We will use the prefix to bind it back to instance
                    prefix='respuesta-{}'.format(respuesta_obj.id),
                    pregunta=pregunta['id'])

            pregunta['respuestas'] = respuestas
            pregunta['opciones_respuesta'] = opciones_respuesta

        subseccion['preguntas'] = preguntas

    context['data'] = subsecciones
    context['id_estudio'] = id_estudio

    if request.method == 'POST':
        max_num_sections = Seccion.objects.all().count()

        if seccion.numero < max_num_sections:  # Are we in the last section yet?
            return redirect(
                'captura:contestar_estudio',
                id_estudio=id_estudio,
                numero_seccion=seccion.numero)

    return render(request, 'captura/captura_estudio.html', context)
