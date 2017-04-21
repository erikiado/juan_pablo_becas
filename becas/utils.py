import locale
import os
import string
from datetime import date

from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import pagesizes
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static


def generate_letter(response, nombre='Elver Ga', ciclo='2016-2017',
                    curso='2° Preescolar Nuevo Ingreso',
                    porcentaje='15', compromiso='''La Madre de familia se compromete a realizar aseos de
                    salones.\nComienza a realizar pago de la aportación mensual enero 2017'''):
    """ This function receives an HttpResponse which has pdf as content type,
    and builds the pdf for the letter.

    Parameters:
    - nombre: name of the student
    - ciclo: year where the scholarship applies
    - curso: which course will the student be in
    - porcentaje: the percentage of scholarship
    - compromiso: what the family will do for the scholarship

    Check the default parameters for examples.
    """

    doc = SimpleDocTemplate(response, pagesize=pagesizes.letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    letter = []
    logo = os.path.join(settings.BASE_DIR, static('carta/logo.png')[1:])

    locale.setlocale(locale.LC_TIME, 'es_ES')

    formatted_time = '{} del {}'.format(
                        string.capwords(date.today().strftime('%A %d %B')),
                        date.today().strftime('%Y'))

    im = Image(logo, 2*inch, 2*inch)
    letter.append(im)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

    ptext = '<font size=12>%s</font>' % formatted_time
    letter.append(Paragraph(ptext, styles['Normal']))
    letter.append(Spacer(1, 12))

    letter.append(Spacer(1, 12))
    ptext = '<font size=12><b>Instituto San Juan Pablo II</b></font>'
    letter.append(Paragraph(ptext, styles['Normal']))
    letter.append(Spacer(1, 12))

    letter.append(Spacer(1, 12))
    ptext = '<font size=12><b>Presente</b></font>'
    letter.append(Paragraph(ptext, styles['Normal']))
    letter.append(Spacer(1, 12))

    ptext = '''<font size=12> Por medio de la presente manifiesto a ustedes
            mi pleno conocimiento y aceptación, respecto  a la APORTACIÓN (BECA)*
            que esta Institución ha otorgado a mi hija (o) <b>{}</b>.</font>'''.format(nombre)
    letter.append(Paragraph(ptext, styles['Justify']))
    letter.append(Spacer(1, 12))

    ptext = '''<font size=12>Él (ella) se inscribirá en esta Institución y
            cursará para el ciclo {} en <b>{}</b>.</font>'''.format(ciclo, curso)
    letter.append(Paragraph(ptext, styles['Justify']))
    letter.append(Spacer(1, 12))

    colwidths = [5*inch, 1.5*inch]
    tbl = []
    ptext = '<font size=12>COSTO VALOR DE EDUCACIÓN EN NUESTRO INSTITUTO</font>'
    tbl.append([Paragraph(ptext, styles['Justify'])])

    ptext = '<font size=12>$2000</font>'
    tbl[0].append(Paragraph(ptext, styles['Center']))

    letter.append(Table(tbl, colWidths=colwidths))
    letter.append(Spacer(1, 15))

    ptext = '<font size=12>Dicha beca se integra de la siguiente manera:</font>'
    letter.append(Paragraph(ptext, styles['Justify']))
    letter.append(Spacer(1, 12))

    tbl = []
    ptext = '<font size=12>PORCENTAJE DE BECA OTORGADO</font>'
    tbl.append([Paragraph(ptext, styles['Normal'])])

    ptext = '<font size=12>%{}</font>'.format(porcentaje)
    tbl[0].append(Paragraph(ptext, styles['Center']))
    letter.append(Table(tbl, colWidths=colwidths))
    letter.append(Spacer(1, 12))

    tbl = []
    ptext = '<font size=12>APORTACIÓN MENSUAL</font>'
    tbl.append([Paragraph(ptext, styles['Normal'])])

    ptext = '<font size=12>$1500</font>'
    tbl[0].append(Paragraph(ptext, styles['Center']))
    letter.append(Table(tbl, colWidths=colwidths))
    letter.append(Spacer(1, 15))

    ptext = '''<font size=12>Comité de Becas autoriza, revisa y califica los
            Estudios Socioeconómico. </font>'''
    letter.append(Paragraph(ptext, styles['Normal']))
    letter.append(Spacer(1, 30))

    ptext = '''<font size=12>Igualmente estoy consciente y acepto las
            condiciones del Reglamento Escolar de la Institución.</font>'''
    letter.append(Paragraph(ptext, styles['Justify']))
    letter.append(Spacer(1, 12))

    ptext = '''<font size=12><b>{}</b></font>'''.format(compromiso)
    letter.append(Paragraph(ptext, styles['Justify']))
    letter.append(Spacer(1, 12))

    ptext = '<font size=12>Atentamente</font>'
    letter.append(Paragraph(ptext, styles['Normal']))
    letter.append(Spacer(1, 20))

    ptext = '<font size=12>___________________</font>'
    letter.append(Paragraph(ptext, styles['Normal']))
    letter.append(Spacer(1, 12))

    ptext = '<font size=11>Nombre y firma del padre, madre y/o tutor</font>'
    letter.append(Paragraph(ptext, styles['Normal']))
    letter.append(Spacer(1, 17))

    ptext = '''<font size=11><b>*La aportación-beca está sujeta a cambios y a
            revisión por el Instituto de Educación Integral IAP y el Comité de Becas,
            en caso de encontrar algún dato falso, la escuela cancelará la beca
            otorgada.</b></font>'''
    letter.append(Paragraph(ptext, styles['Normal']))

    doc.build(letter)
