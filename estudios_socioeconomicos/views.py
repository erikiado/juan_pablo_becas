import csv
import json
from collections import OrderedDict

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse

from rest_framework.response import Response


from captura.utils import get_study_info
from perfiles_usuario.utils import is_capturista, is_member, ADMINISTRADOR_GROUP, CAPTURISTA_GROUP
from perfiles_usuario.utils import is_administrador
from familias.models import Integrante
from familias.utils import total_egresos_familia, total_ingresos_familia, total_neto_familia
from indicadores.models import Transaccion, Ingreso

from .models import Estudio, Foto
from .serializers import EstudioSerializer


                

@login_required
@user_passes_test(is_administrador)
def download_studies(request, id_estudio=None):
    """
    """
    serializer = EstudioSerializer(Estudio.objects.all(), many=True)

    response = HttpResponse(serializer.data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    
    writer = csv.writer(response)
    
    
    return response 

@login_required
@user_passes_test(lambda u: is_member(u, [ADMINISTRADOR_GROUP, CAPTURISTA_GROUP]))
def focus_mode(request, id_estudio):
    """ View to see the detail information about a family and their study.
    """
    context = {}

    estudio = get_object_or_404(Estudio.objects.filter(pk=id_estudio))

    if is_capturista(request.user):
        get_object_or_404(
            Estudio.objects.filter(pk=id_estudio),
            capturista=request.user.capturista)

    integrantes = Integrante.objects.filter(familia=estudio.familia).select_related()
    fotos = Foto.objects.filter(estudio=id_estudio)
    context['estudio'] = estudio
    context['integrantes'] = integrantes
    context['fotos'] = fotos

    context['total_egresos_familia'] = total_egresos_familia(estudio.familia.id)
    context['total_ingresos_familia'] = total_ingresos_familia(estudio.familia.id)
    context['total_neto_familia'] = total_neto_familia(estudio.familia.id)

    transacciones = Transaccion.objects.filter(es_ingreso=True, familia=estudio.familia)
    context['ingresos'] = Ingreso.objects.filter(transaccion__in=transacciones)
    context['egresos'] = Transaccion.objects.filter(es_ingreso=False, familia=estudio.familia)
    context['cuestionario'] = get_study_info(estudio)
    context['status_options'] = Estudio.get_options_status()
    return render(
        request,
        'estudios_socioeconomicos/focus_mode.html',
        context)
