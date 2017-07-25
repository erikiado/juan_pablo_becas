import locale
import string
import decimal
from datetime import date

from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib import pagesizes
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from administracion.models import Colegiatura


def generate_letter(response, nombre='Juan Perez', ciclo='2016-2017',
                    grado='2° Preescolar Nuevo Ingreso', porcentaje='15',
                    compromiso='''La Madre de familia se compromete a realizar aseos
                    de salones.''', a_partir='''Comienza a realizar pago de la aportación
                    mensual enero 2017'''):
    """ This function receives an HttpResponse which has pdf as content type,
    and builds the pdf for the letter.

    Parameters:
    - nombre: name of the student
    - ciclo: year where the scholarship applies
    - grado: which course will the student be in
    - porcentaje: the percentage of scholarship
    - compromiso: what the family will do for the scholarship
    - a_partir: from when does the family start paying.

    Check the default parameters for examples.
    """

    doc = SimpleDocTemplate(response, pagesize=pagesizes.letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=110, bottomMargin=18)
    letter = []
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    formatted_time = '{} del {}'.format(
                        string.capwords(date.today().strftime('%A %d %B')),
                        date.today().strftime('%Y'))

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))

    ptext = '<font size=12>%s</font>' % formatted_time
    letter.append(Paragraph(ptext, styles['Right']))
    letter.append(Spacer(1, 12))

    letter.append(Spacer(1, 12))
    ptext = '<font size=12><b>Carta de Comunicación de Beca Otorgada</b></font>'
    letter.append(Paragraph(ptext, styles['Normal']))
    letter.append(Spacer(1, 12))

    letter.append(Spacer(1, 12))
    ptext = '<font size=12><b>Presente</b></font>'
    letter.append(Paragraph(ptext, styles['Normal']))
    letter.append(Spacer(1, 35))

    ptext = '''<font size=12> Por medio de la presente manifiesto a ustedes
            mi pleno conocimiento y aceptación, respecto  a la APORTACIÓN (BECA)*
            que esta Institución ha otorgado a mi hija (o) <b>{}</b>.</font>'''.format(nombre)
    letter.append(Paragraph(ptext, styles['Justify']))
    letter.append(Spacer(1, 12))

    ptext = '''<font size=12>Él (ella) se inscribirá en esta Institución y
            cursará para el ciclo {} en <b>{}</b>.</font>'''.format(ciclo, grado)
    letter.append(Paragraph(ptext, styles['Justify']))
    letter.append(Spacer(1, 12))

    ptext = '<font size=12>Dicha beca se integra de la siguiente manera:</font>'
    letter.append(Paragraph(ptext, styles['Justify']))
    letter.append(Spacer(1, 20))

    colwidths = [5.2*inch, 1.3*inch]
    tbl = []
    ptext = '<font size=12>COSTO VALOR DE EDUCACIÓN EN NUESTRO INSTITUTO</font>'
    tbl.append([Paragraph(ptext, styles['Justify'])])

    colegiatura = Colegiatura.objects.all()[0]
    ptext = '<font size=12>{}</font>'.format(colegiatura)
    tbl[0].append(Paragraph(ptext, styles['Normal']))

    letter.append(Table(tbl, colWidths=colwidths))
    letter.append(Spacer(1, 15))

    tbl = []
    ptext = '<font size=12>PORCENTAJE DE BECA OTORGADO</font>'
    tbl.append([Paragraph(ptext, styles['Justify'])])

    ptext = '<font size=12>{}</font>'.format(porcentaje)
    tbl[0].append(Paragraph(ptext, styles['Normal']))
    letter.append(Table(tbl, colWidths=colwidths))
    letter.append(Spacer(1, 12))

    tbl = []
    ptext = '<font size=12>APORTACIÓN MENSUAL</font>'
    tbl.append([Paragraph(ptext, styles['Normal'])])

    monto = colegiatura.monto
    aportacion = monto - (monto*decimal.Decimal(porcentaje[:-1])/decimal.Decimal('100.0'))
    ptext = '<font size=12>${}</font>'.format(aportacion)
    tbl[0].append(Paragraph(ptext, styles['Normal']))
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

    ptext = '''<font size=12><b>{}</b></font>'''.format(a_partir)
    letter.append(Paragraph(ptext, styles['Justify']))
    letter.append(Spacer(1, 23))

    ptext = '<font size=12>Atentamente</font>'
    letter.append(Paragraph(ptext, styles['Normal']))
    letter.append(Spacer(1, 20))

    ptext = '<font size=12>_______________________________</font>'
    letter.append(Paragraph(ptext, styles['Normal']))
    letter.append(Spacer(1, 12))

    ptext = '<font size=11>Nombre y firma del padre, madre y/o tutor</font>'
    letter.append(Paragraph(ptext, styles['Normal']))
    letter.append(Spacer(1, 17))

    ptext = '''<font size=11>*La aportación-beca está sujeta a cambios y a
            revisión por el Instituto de Educación Integral IAP y el Comité de Becas,
            en caso de encontrar algún dato falso, la escuela cancelará la beca
            otorgada.</font>'''
    letter.append(Paragraph(ptext, styles['Normal']))

    doc.build(letter)


def aportacion_por_beca(beca):
    colegiatura = Colegiatura.objects.all()[0]
    porcentaje = beca.porcentaje

    aportacion = (100.0 - float(porcentaje)) * float(colegiatura.monto) / 100.0

    return '${:.2f}'.format(aportacion)
