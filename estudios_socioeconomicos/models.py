from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

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
    RECHAZADO = 'rechazado'  # rejected from the POV of the admin
    BORRADOR = 'borrador'  # draft of a capturista
    REVISION = 'revision'  # the admin has to check it
    ELIMINADO = 'eliminado'
    OPCIONES_STATUS = ((APROBADO, 'Aprobado'),
                       (RECHAZADO, 'Rechazado'),
                       (BORRADOR, 'Borrador'),
                       (REVISION, 'Revisión'),
                       (ELIMINADO, 'Eliminado'))

    capturista = models.ForeignKey(Capturista)
    familia = models.OneToOneField(Familia)
    status = models.TextField(choices=OPCIONES_STATUS, default=BORRADOR)

    def __str__(self):
        return '{familia}'.format(familia=self.familia.__str__())

    @staticmethod
    def get_options_status():
        """ Returns a dictionary with the options for status to be used in the templates.

        """
        return {
            'APROBADO': Estudio.APROBADO,
            'BORRADOR': Estudio.BORRADOR,
            'ELIMINADO': Estudio.ELIMINADO,
            'REVISION': Estudio.REVISION,
            'RECHAZADO': Estudio.RECHAZADO
        }

class Foto(models.Model):
    """
    """
    estudio = models.ForeignKey(Estudio, on_delete=models.CASCADE)

    file_name = models.CharField(max_length=100)
    upload = models.FileField(upload_to='')
    is_active = models.BooleanField(default=True)

@receiver(post_save, sender=Estudio)
def create_answers_for_study(sender, instance=None, created=False, **kwargs):
    """ Signal for creating all answers for all questions on a new study.

    This triggers creates all answer objects for all existing questions on a new
    study. Since we are dealing with de-normalized data for the questions stored
    in the database, we want to populate all the answers to query them and display
    them to the user.

    When we create a study through a REST endpoint for an offline client we dont
    want to create all answers (the client will already providing them). We can skip
    this trigger using .save_base(raw=True) on a estudio object.

    Parameters:
    -----------
      instance : estudios_socioeconomicos.models.Estudio
          The instance of the object whose creation triggered the signal. In this case a
          Estudio.
      created : BooleanField
          A value indicating if this instance is being created for the first time. Or if set
          to false if it is being edited.

      kwargs['raw']: BooleanField
        A value indicating us if we can skip the trigger.
    """
    raw = kwargs['raw']
    if created and not raw:
        preguntas = Pregunta.objects.all()
        for pregunta in preguntas:
            Respuesta.objects.create(estudio=instance, pregunta=pregunta)


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
    seccion = models.ForeignKey(Seccion, related_name='subsecciones')

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
    """
    subseccion = models.ForeignKey(Subseccion, null=True, related_name='preguntas')

    texto = models.TextField()
    descripcion = models.TextField(blank=True)
    orden = models.IntegerField(default=0)

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
    pregunta = models.ForeignKey(Pregunta, related_name='opciones_pregunta')

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
    estudio = models.ForeignKey(Estudio, related_name='respuesta_estudio')
    pregunta = models.ForeignKey(Pregunta, related_name='respuesta_pregunta')
    eleccion = models.OneToOneField(OpcionRespuesta, null=True, blank=True)
    integrante = models.ForeignKey(Integrante, null=True, blank=True)

    respuesta = models.TextField(blank=True)

    def __str__(self):
        """ String representation of the answer.

        If the answer has text, we print the text. Otherwise,
        we print the option chosen for the answer.
        If it is empty, we return a string indicating so.
        """
        if self.respuesta:
            return self.respuesta
        elif self.eleccion:
            return str(self.eleccion)
        else:
            return 'No tiene respuesta.'
