from django.db import models
from familias.models import Familia, Integrante
from perfiles_usuario.models import Capturista


class Estudio(models.Model):
    """ The model that represents a socioeconomical study.

    This model contains the relations to link families and the actual
    information stored for each study.

    Attributes:
    -----------
    OPCIONES_STATUS : tuple(tuple())
        The options for the current status of a study.
    capturista : ForeignKey
        The relation to the capturista that filled the study.
    familia : OneToOneField
        The family of which the study is about.
    status : TextField
        The study can be in several states depending if it has been approved,
        is on revision, has been rejected, is a draft or was deleted.
    numero_sae : TextField
        TODO: more information on this field. It appears to be some sort of
        id for studies (refer to the sample study provided by the stakeholder).
    """
    APROBADO = 'aprobado'
    RECHAZADO = 'rechazado'
    BORRADOR = 'borrador'
    REVISION = 'revision'
    ELIMINADO = 'eliminado'
    OPCIONES_STATUS = ((APROBADO, 'Aprobado'),
                       (RECHAZADO, 'Rechazado'),
                       (BORRADOR, 'Borrador'),
                       (REVISION, 'Revisión'),
                       (ELIMINADO, 'Eliminado'))

    capturista = models.ForeignKey(Capturista)
    familia = models.OneToOneField(Familia)

    status = models.TextField(choices=OPCIONES_STATUS)
    numero_sae = models.TextField(blank=True)

    def __str__(self):
        return '{familia} status: {status}'.format(
                                familia=self.familia.__str__(),
                                status=self.status)


class Seccion(models.Model):
    """ The model that links questions to a particular section.

    Attributes:
    -----------
    nombre : TextField
        The name of the section.
    numero : IntegerField
        The number of the section.
    """
    nombre = models.TextField()
    numero = models.IntegerField()

    def __str__(self):
        return 'Sección {nombre} número {num}'.format(nombre=self.nombre, num=self.numero)


class Subseccion(models.Model):
    """ The model that represents a subsection within a section.

    Attributes:
    -----------
    nombre : TextField
        The name of the subsection.
    numero : IntegerField
        The number of the section.
    """
    seccion = models.ForeignKey(Seccion)

    nombre = models.TextField()
    numero = models.IntegerField()

    def __str__(self):
        return 'Subsección {nombre}, en {seccion}'.format(
                                nombre=self.nombre,
                                seccion=str(self.seccion))


class Pregunta(models.Model):
    """ The model that stores the actual questions.

    Attributes:
    -----------
    subseccion : ForeignKey
        The subsection to which the question belongs.
    texto : TextField
        The question itself.
    descripcion : TextField
        Additional information that the question may need to have.
    orden : IntegerField
        The relative order of the question within the subsection.
    relacionado_a_integrante : BooleanField
        Indicates whether the answer of this question needs to be related
        with a family member. This is important for rendering the form and
        determining if the relationship between answer and family member should exist.
    """
    subseccion = models.ForeignKey(Subseccion, null=True)

    texto = models.TextField()
    description = models.TextField(blank=True)
    orden = models.IntegerField(default=0)
    relacionado_a_integrante = models.BooleanField(default=False)

    def __str__(self):
        return self.texto


class OpcionRespuesta(models.Model):
    """ The model that stores options for a particular question.

    Attributes:
    -----------
    pregunta : ForeignKey
        The question for which these options are provided.
    texto : TextField
        The option for answer itself.
    """
    pregunta = models.ForeignKey(Pregunta)

    texto = models.TextField()

    def __str__(self):
        return self.texto


class Respuesta(models.Model):
    """ The model that stores the actual answers.

    This model is the actual information from a study. Note that it
    can be related to an answer option, or to a family member, but both
    relations are not mandatory.

    Attributes:
    -----------
    estudio : ForeignKey
        The study to which these answers belong.
    pregunta : ForeignKey
        The question this answer is responding to.
    opcion : ManyToManyField
        Optional relation to the options of the question, if the question
        requires them. It's a many to many rel. instead of a one to many since
        the question may need more than one option.
    integrante : ForeignKey
        If the question is related to a particular family member, this relationship
        indicates to which one.
    respuesta : TextField
        If the answer needs to have text, it will be stored in this attribute.
    """
    estudio = models.ForeignKey(Estudio)
    pregunta = models.ForeignKey(Pregunta)
    elecciones = models.ManyToManyField(OpcionRespuesta, blank=True)
    integrante = models.ForeignKey(Integrante, null=True, blank=True)

    respuesta = models.TextField(blank=True)

    def __str__(self):
        """ String representation of the answer.

        If the answer has text, we print the text. Otherwise,
        we concatenate the options chosen for the answer.
        If it is empty, we return a string indicating so.
        """
        if self.respuesta:
            return self.respuesta
        elif self.elecciones.all():
            return ', '.join(sorted(map(str, self.elecciones.all())))
        else:
            return 'No tiene respuesta.'
