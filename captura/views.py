from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse

from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from administracion.models import Escuela
from perfiles_usuario.utils import is_capturista
from perfiles_usuario.models import Capturista
from estudios_socioeconomicos.forms import DeleteEstudioCapturistaForm, RespuestaForm
from estudios_socioeconomicos.serializers import SeccionSerializer, EstudioSerializer
from estudios_socioeconomicos.serializers import FotoSerializer
from estudios_socioeconomicos.models import Respuesta, Pregunta, Seccion, Estudio, Foto
from familias.forms import FamiliaForm, IntegranteForm, IntegranteModelForm, DeleteIntegranteForm
from familias.models import Familia, Integrante
from familias.utils import total_egresos_familia, total_ingresos_familia, \
                           total_neto_familia
from familias.serializers import EscuelaSerializer
from indicadores.serializers import OficioSerializer
from indicadores.models import Transaccion, Ingreso, Oficio
from indicadores.forms import TransaccionForm, IngresoForm
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

    Returns
    ----------
    GET:
        On succes returns HTTP 200 with captura/captura_base.html
        template rendeered, this template contains an empty form
        for integrante.

        On error returns HTTP 500

    POST:
        On succes returns HTTP 301 redirect to the integrantes table.
        On error returns to the same form but with errors.
    """

    form = None
    if request.method == 'POST':
        form = FamiliaForm(request.POST)
        if form.is_valid():
            form.save()
            Estudio.objects.create(capturista=request.user.capturista, familia=form.instance)
            return redirect(reverse('captura:list_integrantes',
                                    kwargs={'id_familia': form.instance.pk}))
    context = {}
    if form:
        context['form'] = form
    else:
        context['form'] = FamiliaForm()
    context['form_view'] = 'captura/familia_form.html'
    context['create'] = True
    return render(request, 'captura/captura_base.html', context)


@login_required
@user_passes_test(is_capturista)
def estudio_delete_modal(request, id_estudio):
    """ View to send the form to delete users.

    When a user accesses this view, it returns the form required to
    confirm the soft delition of a study, along with all of its
    information.

    Returns
    ----------
    GET:
        On succes returns HTTP 200 with estudio_socioeconomicos/estudio_delete_modal.html
        template rendeered, this template contains a confirmation form for the soft
        delition of a estudio socioeconomico

        On error returns HTTP 404
    """
    if request.is_ajax():
        estudio = get_object_or_404(Estudio, pk=id_estudio)
        form = DeleteEstudioCapturistaForm(initial={'id_estudio': estudio.pk})
        return render(request, 'estudios_socioeconomicos/estudio_delete_modal.html',
                      {'estudio_to_delete': estudio, 'delete_form': form})
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_capturista)
def estudio_delete(request):
    """ View to delete estudio.

    """
    if request.method == 'POST':
        form = DeleteEstudioCapturistaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('captura:estudios')
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_capturista)
def recover_studies(request):
    """ View to list the studies that are deleted and can be recovered.

    """
    estudios = Estudio.objects.filter(capturista=request.user.capturista,
                                      status=Estudio.ELIMINADO_CAPTURISTA)
    context = {
        'estudios': estudios
    }
    return render(request, 'captura/recuperar_estudios.html', context)


@login_required
@user_passes_test(is_capturista)
def edit_familia(request, id_familia):
    """ This view allows a capturista to capture the information related
    to a specific family.

    Returns
    ----------
    GET:
        On succes returns HTTP 200 with captura/captura_base.html
        template rendeered, this template contains an empty form
        for integrante.

        On error returns HTTP 500

    POST:
        On succes returns HTTP 301 redirect to the integrantes table.
        On error returns to the same form but with errors.
    """
    form = None
    if request.method == 'POST':
        instance = get_object_or_404(Familia, pk=id_familia)
        form = FamiliaForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse('captura:list_integrantes',
                                    kwargs={'id_familia': form.instance.pk}))
    context = {}
    context['familia'] = Familia.objects.get(pk=id_familia)
    if form:
        context['form'] = form
    else:
        context['form'] = FamiliaForm(instance=context['familia'])
    context['form_view'] = 'captura/familia_form.html'
    return render(request, 'captura/captura_base.html', context)


@login_required
@user_passes_test(is_capturista)
def list_integrantes(request, id_familia):
    """ This view allows a capturista to see all the information about the
    integrantes of a specific family, they are displayed inside a table,
    and the capturista can select each of them individually.
    """
    context = {}

    integrantes = Integrante.objects.filter(familia__pk=id_familia, activo=True)
    familia = Familia.objects.get(pk=id_familia)
    context['integrantes'] = integrantes
    context['familia'] = familia
    context['create_integrante_form'] = IntegranteModelForm()
    context['id_familia'] = id_familia
    return render(request, 'captura/dashboard_integrantes.html', context)


@login_required
@user_passes_test(is_capturista)
def create_edit_integrante(request, id_familia):
    """ View to create and edit integrantes.

    This receives an ajax request made submitting the form.
    If we want to create a user, the field 'id_integrante' will be empty.
    Otherwise, it will have the id of the Integrante.
    """
    if request.is_ajax() and request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['familia'] = id_familia
        form = None
        response_data = {}
        if request.POST['id_integrante']:  # to edit integrantes
            integrante = Integrante.objects.get(pk=request.POST['id_integrante'])
            form = IntegranteModelForm(request.POST, instance=integrante)
            response_data['msg'] = 'Integrante Editado'
        else:  # to create an integrante
            form = IntegranteModelForm(request.POST)
            response_data['msg'] = 'Integrante Creado'
        if form.is_valid():
            integrante = form.save()
            return JsonResponse(response_data)
        else:
            return HttpResponse(form.errors.as_json(), status=400, content_type='application/json')


@login_required
@user_passes_test(is_capturista)
def get_form_edit_integrante(request, id_integrante):
    """ View that is called via ajax to render the partially
    loaded form to edit an integrante.

    We return the id_integrante which is used in create_edit_integrante.
    """
    if request.is_ajax() and request.method == 'GET':
        integrante = Integrante.objects.get(pk=id_integrante)
        initial_data = {}
        rol = IntegranteForm.OPCION_ROL_NINGUNO
        if hasattr(integrante, 'alumno_integrante'):  # check reverse relation w/alumno
            rol = IntegranteForm.OPCION_ROL_ALUMNO
            initial_data['numero_sae'] = integrante.alumno_integrante.numero_sae
            initial_data['escuela'] = integrante.alumno_integrante.escuela
        elif hasattr(integrante, 'tutor_integrante'):  # check reverse relation w/tutor
            rol = IntegranteForm.OPCION_ROL_TUTOR
            initial_data['relacion'] = integrante.tutor_integrante.relacion
        initial_data['rol'] = rol
        form = IntegranteModelForm(instance=integrante, initial=initial_data)
        context = {
            'create_integrante_form': form,
            'id_familia': integrante.familia.pk,
            'id_integrante': id_integrante
        }
        return render(request, 'captura/create_integrante_form.html', context)


@login_required
@user_passes_test(is_capturista)
def get_form_delete_integrante(request, id_integrante):
    """ View that is called via ajax to render the modal
    to confirm the deletion of an Integrante.

    """
    if request.is_ajax() and request.method == 'GET':
        integrante = get_object_or_404(Integrante, pk=id_integrante)
        form = DeleteIntegranteForm(initial={'id_integrante': integrante.pk})
        context = {
            'integrante': integrante,
            'delete_form': form
        }
        return render(request, 'captura/integrante_delete_modal.html', context)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_capturista)
def delete_integrante(request, id_integrante):
    """ This view receives the form to delete an integrante
    and redirects to the listing of integrantes.
    """
    if request.method == 'POST':
        form = DeleteIntegranteForm(request.POST)
        integrante = get_object_or_404(Integrante, pk=id_integrante)
        if form.is_valid():
            form.save()
        return redirect('captura:list_integrantes', id_familia=integrante.familia.pk)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_capturista)
def update_create_transaccion(request, id_familia):
    """ This view allows any user to create a new transaccion
    regardless of it's type either ingreso or egreso.

    """
    if request.is_ajax() and request.method == 'POST':
        response_data = {}
        if request.POST.get('id_transaccion', None):  # In case of updating
            transaccion = get_object_or_404(Transaccion, pk=request.POST['id_transaccion'])
            transaccion_form = TransaccionForm(request.POST, instance=transaccion)
        else:  # In case of creation
            transaccion_form = TransaccionForm(request.POST)
        if transaccion_form.is_valid():
            transaccion_form.save()
            if transaccion_form.cleaned_data['es_ingreso']:
                if hasattr(transaccion_form.instance, 'ingreso'):  # In case of updating
                    ingreso_form = IngresoForm(id_familia, request.POST,
                                               instance=transaccion_form.instance.ingreso)
                else:
                    ingreso_form = IngresoForm(id_familia, request.POST)
                if ingreso_form.is_valid():
                    ingreso = ingreso_form.save(commit=False)
                    ingreso.transaccion = transaccion_form.instance
                    ingreso.save()
                    response_data['msg'] = 'Ingreso guardado con éxito'
                    return JsonResponse(response_data)
                return HttpResponse(ingreso_form.errors.as_json(),
                                    status=400,
                                    content_type='application/json')
            response_data['msg'] = 'Egreso guardado con éxito'
            return JsonResponse(response_data)
        return HttpResponse(transaccion_form.errors.as_json(),
                            status=400,
                            content_type='application/json')
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_capturista)
def update_transaccion_modal(request, id_transaccion):
    """ Returns a form that can be used to edit an existing
    transaccion.
    """
    if request.is_ajax():
        context = {}
        transaccion = get_object_or_404(Transaccion, pk=id_transaccion)
        id_familia = transaccion.familia.pk
        context['id_familia'] = id_familia
        id_transaccion = transaccion.pk
        context['transaccion_form'] = TransaccionForm(instance=transaccion,
                                                      initial={'id_transaccion': id_transaccion})
        if hasattr(transaccion, 'ingreso'):
            context['ingreso_form'] = IngresoForm(id_familia, instance=transaccion.ingreso)
        return render(request, 'captura/edit_ingreso_egreso_form.html', context)
    return HttpResponseBadRequest()


@login_required
@user_passes_test(is_capturista)
def delete_transaccion(request):
    """ This view soft deletes a transaccion from the family, so it can be
    ignored in caclulations about their current economic status, but a history
    can be still be retrieved.
    """
    pass


@login_required
@user_passes_test(is_capturista)
def list_transacciones(request, id_familia):
    """ This view allows a capturista to see all the financial information
    of a specific family, they are displayed inside a table, and this view is
    also the interface for the CRUD of transactions.
    """
    context = {}
    context['familia'] = get_object_or_404(Familia, pk=id_familia)
    context['total_egresos_familia'] = total_egresos_familia(id_familia)
    context['total_ingresos_familia'] = total_ingresos_familia(id_familia)
    context['total_neto_familia'] = total_neto_familia(id_familia)
    transacciones = Transaccion.objects.filter(es_ingreso=True, familia=context['familia'])
    context['ingresos'] = Ingreso.objects.filter(transaccion__in=transacciones)
    context['egresos'] = Transaccion.objects.filter(es_ingreso=False, familia=context['familia'])
    context['create_egreso_form'] = TransaccionForm(initial={'es_ingreso': False,
                                                             'familia': context['familia']})
    context['create_transaccion_form'] = TransaccionForm(initial={'es_ingreso': True,
                                                                  'familia': context['familia']})
    context['create_ingreso_form'] = IngresoForm(id_familia)
    return render(request, 'captura/dashboard_transacciones.html', context)


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


class APIOficioInformation(generics.ListAPIView):
    """ API to get all available oficios.

        Retrieves all objects from database.

        Returns
        --------
        JSON object with Oficio objects.
    """
    serializer_class = OficioSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Oficio.objects.all()


class APIEscuelaInformation(generics.ListAPIView):
    """ API to get all available escuelas.

        Retrieves all objects from database.

        Returns
        --------
        JSON object with Escuela objects.
    """
    serializer_class = EscuelaSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Escuela.objects.all()


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
            return Response(EstudioSerializer(instance).data, status.HTTP_201_CREATED)

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


class APIUploadRetrieveImages(viewsets.ViewSet):
    """ API ViewSet for offline client to submit images to a study.

        This view handles all REST operations for an offline client
        to upload questions for a study.
    """
    def list(self, request, id_estudio):
        """ Retrieves all Photos in a given study that belong to
            the Capturista making the Query.

            Raises
            ------
            HTTP STATUS 404
            If there are no photos for the study or the capturista
            does not have access to a specific study being queried.

            Returns
            -------
            Response
                Response object containing the serializer data
        """
        queryset = Estudio.objects.filter(capturista=request.user.capturista)
        estudio = get_object_or_404(queryset, pk=id_estudio)

        queryset = Foto.objects.filter(estudio=estudio)
        serializer = FotoSerializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, id_estudio):
        """ Creates and saves a new Foto object for an estudio.

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
        queryset = Estudio.objects.filter(capturista=request.user.capturista)
        get_object_or_404(queryset, pk=request.POST['estudio'])

        serializer = FotoSerializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.create(serializer.validated_data)
            return Response(FotoSerializer(instance).data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
