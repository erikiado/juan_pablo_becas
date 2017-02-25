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
        return self.familia.__str__()

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

class Pregunta(models.Model):
    """ The model that stores the actual questions.

    Attributes:
    -----------
    seccion : ForeignKey
        The section to which the question belongs.
    texto : TextField
        The question itself.
    """
    seccion = models.ForeignKey(Seccion)

    texto = models.TextField()

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
    estudio = models.ForeignKey(Estudio)
    opcion = models.ManyToManyField(OpcionRespuesta)
    pregunta = models.ForeignKey(Pregunta)
    integrante = models.ForeignKey(Integrante)
    respuesta = models.TextField(blank=True)

    def __str__(self):
        return self.respuesta if self.respuesta else self.opcion.texto
