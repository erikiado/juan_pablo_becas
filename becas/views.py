from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http.response import HttpResponseBadRequest
from django.http import HttpResponse
from django.conf import settings

from familias.utils import total_egresos_familia, total_ingresos_familia, total_neto_familia
from familias.models import Integrante
from perfiles_usuario.utils import is_administrador
from estudios_socioeconomicos.models import Estudio, Foto

from .forms import BecaForm
from .models import Beca


@login_required
def estudios(request):
    """ DUMMY VIEW.

    This functions is currently just being used to test the redirect
    from base.

    TODO: name properly and implement everything
    """
    return render(request, 'layouts/dashboard_base.html')


@login_required
@user_passes_test(is_administrador)
def asignar_beca(request, id_estudio):
    """ GET: Renders the view where the admin assigns the scholarship
    to a family after approving a study.

    POST: Validates the form and creates scholarships for all
    students associated to the study.
    """
    estudio = get_object_or_404(Estudio, pk=id_estudio, status=Estudio.APROBADO)
    fotos = Foto.objects.filter(estudio=id_estudio)
    integrantes = Integrante.objects.filter(familia__pk=estudio.familia.pk, activo=True)
    integrantes = filter(lambda x: hasattr(x, 'alumno_integrante'), integrantes)
    context = {
        'estudio': estudio,
        'total_egresos_familia': total_egresos_familia(estudio.familia.id),
        'total_ingresos_familia': total_ingresos_familia(estudio.familia.id),
        'total_neto_familia': total_neto_familia(estudio.familia.id),
        'fotos': fotos,
        'integrantes': integrantes
    }
    if request.method == 'GET':
        context['form'] = BecaForm()
        return render(request, 'becas/asignar_beca.html', context)
    elif request.method == 'POST':
        form = BecaForm(request.POST)
        if form.is_valid():
            percentage = form.cleaned_data['porcentaje']
            # create scholarships for active students
            for integrante in integrantes:
                Beca.objects.create(alumno=integrante.alumno_integrante,
                                    porcentaje=percentage)
            return redirect('estudios_socioeconomicos:focus_mode', id_estudio=id_estudio)
        else:
            context['form'] = form
            return render(request, 'becas/asignar_beca.html', context)
    return HttpResponseBadRequest()


def carta_beca(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    from datetime import date
    import locale
    import os
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from django.contrib.staticfiles.templatetags.staticfiles import static
     
    doc = SimpleDocTemplate(response, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    Story = []
    logo = os.path.join(settings.BASE_DIR, static('carta/logo.png')[1:])
     
    locale.setlocale(locale.LC_TIME, 'es_ES')
    import string
    formatted_time = '{} del {}'.format(
                        string.capwords(date.today().strftime('%A %d %B')),
                        date.today().strftime('%Y'))
    address_parts = ["411 State St.", "Marshalltown, IA 50158"]
     
    im = Image(logo, 2*inch, 2*inch)
    Story.append(im)
     
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size=12>%s</font>' % formatted_time
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
     
    Story.append(Spacer(1, 12))
    ptext = '<font size=12><b>Instituto San Juan Pablo II</b></font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))  
     
    Story.append(Spacer(1, 12))
    ptext = '<font size=12><b>Presente</b></font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
     
    nombre = 'Juan Pablo Cristobal Martínez'
    ptext = '''<font size=12> Por medio de la presente manifiesto a ustedes 
            mi pleno conocimiento y aceptación, respecto  a la APORTACIÓN (BECA)*  
            que esta Institución ha otorgado a mi hija (o) <b>{}</b>.</font>'''.format(nombre)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    curso = '2° Preescolar Nuevo Ingreso'
    ptext = '''<font size=12>Él (ella) se inscribirá en esta Institución y 
            cursará para el ciclo  2016-2017 en <b>{}</b>.</font>'''.format(curso)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
     
     
    ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
    ptext = '<font size=12>Sincerely,</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 48))
    ptext = '<font size=12>Ima Sucker</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    doc.build(Story)
    return response
