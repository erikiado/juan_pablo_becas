from django.db import models
from core.validators import PHONE_REGEX
# from administracion.models import Escuela


class Familia(models.Model):
    """ Main model of the family app.

    This models stores the main attributes and indicators
    of a family, it also serves as a HUB for the models
    that store the main data points from the socioeconomical
    studies.

    Attributes:
    -----------
    OPCIONES_ESTADO_CIVIL : tuple(tuple())
        This is a field that stores the list of options to be stored in the
        estado_civil field.
    OPCIONES_LOCALIDAD : tuple(tuple())
        This is a field that stores the list of options to be stored in the localidad field.
    numero_hijos_diferentes_papas : IntegerField
        The content of this field needs to be clarified with the stakeholder, whether this
        is the number of unique parents, the children of a mother have, or just the total
        number of children.
    explicacion_solvencia : TextField
        This field should be filled in their net mensual income is negative. It serves as an
        explanation on how the family deals with the deficit.
    estado_civil : TextField
        This field stores the information regarding the legal relationship status of the
        parents in a family.
    localidad : Text Field
        This field stores the town in which a family resides.

    TODO:
    -----

    - Implement total_neto field, total_egresos, and total_ingresos, once the ingresos and
    egresos tables are created.
    - Clarify the contents of the number_hijos_diferentes_papas field
    """
    OPCIONES_ESTADO_CIVIL = (('soltero', 'Soltero'),
                             ('viudo', 'Viudo'),
                             ('union libre', 'Unión Libre'),
                             ('casado civil', 'Casado-Civil'),
                             ('casado iglesia', 'Casado-Iglesia'),
                             ('vuelto a casar', 'Divorciado Vuelto a Casar'))

    OPCIONES_LOCALIDAD = (('Poblado Jurica', 'Poblado Juríca'),
                          ('Nabo', 'Nabo'),
                          ('Salitre', 'Salitre'),
                          ('La Campana', 'La Campana'),
                          ('otro', 'Otro'))

    numero_hijos_diferentes_papas = models.IntegerField(default=0)
    explicacion_solvencia = models.TextField()
    estado_civil = models.TextField(choices=OPCIONES_ESTADO_CIVIL)
    localidad = models.TextField(choices=OPCIONES_LOCALIDAD)


class Comentario(models.Model):
    """ Comment regarding the economical situation of a family.

    This comments include information that is relevant to the determination of
    the amount of the scholarship awarded to a student e.g. The recent desease
    of a family member. History is mantained via a ManyToMany relationship with
    a family.

    Attributes:
    -----------
    familia : ForeignKey
        This represents the relationship with an instance of the Family class.
    fecha : DateTimeField
        This stores the data about the date of creation of an instantce of this class.
    texto : TextField
        This stores the actual comment that is made about the family's situation.

    TODO:
    -----
    - Determine if this model should have a relationship with an user model.
    """

    familia = models.ForeignKey(Familia)
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.TextField()

    def __str__(self):
        """ Prints the texto attribute of this class.

        """
        return self.texto


class Integrante(models.Model):
    """ This is the parent class for all members of a family.

    Every single member of a family is an instance of this class. Some family may be
    extended with OneToOne relationships to instances of this class.

    Attributes:
    -----------
    OPCIONES_NIVEL_ESTUDIOS : tuple(tuple)
        This are the options for the nivel_studios attribute.
    familia : ForeignKey
        This establishes the pertenence of a family member to a family.
    nombres : TextField
        This attribute stores the name(s) of a family member.
    apellidos : TextField
        This attribute stores the lastname(s) of a family member.
    telefono : CharField
        This attribute stores the phone number of a family member; phone number must
        be compliant with E.164 standard.
    correo : EmailField
        This attribute stores the email of a family member.
    nivel_estudios : TextField
        Stores the scholarity level of a family member.
    fecha_de_nacimiento : DateField
        Store the date of birth of a family member.
    activo: BooleanField
        This attribute stores information about the involvment of a family member
        with the family itself.

    TODO:
    -----
    - Implement foreign key relationship with oficio.
    """

    OPCIONES_NIVEL_ESTUDIOS = (('ninguno', 'Ninguno'),
                               ('1º grado', 'Primero de Primaria'),
                               ('2º grado', 'Segundo de Primaria'),
                               ('3º grado', 'Tercero de Primaria'),
                               ('4º grado', 'Cuarto de Primaria'),
                               ('5º grado', 'Quinto de Primaria'),
                               ('6º grado', 'Sexto de Primaria'),
                               ('7º grado', 'Primero de Secundaria'),
                               ('8º grado', 'Segundo de Secundaria'),
                               ('9º grado', 'Tercero de Secundaria'),
                               ('10º grado', 'Primero de Pecundaria'),
                               ('11º grado', 'Segundo de Preparatoria'),
                               ('12º grado', 'Tercero de Preparatoria'),
                               ('universidad', 'Universidad'),
                               ('maestria', 'Maestría'),
                               ('doctorado', 'Doctorado'))
    familia = models.ForeignKey(Familia)
    nombres = models.TextField()
    apellidos = models.TextField()
    telefono = models.CharField(validators=[PHONE_REGEX], null=True, max_length=16)
    correo = models.EmailField(null=True)
    nivel_estudios = models.TextField(choices=OPCIONES_NIVEL_ESTUDIOS)
    fecha_de_nacimiento = models.DateField()
    activo = models.BooleanField(default=True)


class Alumno(models.Model):
    """ This class extends the Integrante model, creating the Student profile.

    The purpose of this class is to extend the Integrante model, in order to
    store information that is only required of actual students at the
    institution.

    Attributes:
    -----------
    integrante : OneToOneField
        This directly extends the Integrante model, in order to have access to all
        the other information that is stored about all of the family members.

    activo : BooleanField
        This field is different from the activo field in integrante, this field
        marks whether the student is currently enrolled at the institution or not.
    escuela : ForeignKey
        This field stores the actual school in which the student is enrolled, or is
        planned to attend once the inscription process is over.

    TODO: activate the ManyToOne with Escuela once the model is declared in the
    administracion app.
    """

    integrante = models.OneToOneField(Integrante)
    activo = models.BooleanField(default=True)
    # escuela = models.ForeignKey(Escuela)


class Tutor(models.Model):
    """ This class extends the Integrante model, creating the Tutor profile.

    The purpose of this class is to extend the Integrante model, in order
    to store information that is only required of the tutors of students.

    Attributes:
    -----------
    OPCIONES_RELACION : tuple(tuple)
        This attribute stores all the options for the relacoin field.
    integrante : OneToOneField
        This directly extends the Integrante model, in order to have access to all
        the other information that is stored about all of the family members.
    relacion : TextField
    """
    OPCIONES_RELACION = (('madre', 'Madre'),
                         ('padre', 'Padre'),
                         ('tutor', 'Tutor'))
    integrante = models.OneToOneField(Integrante)
    relacion = models.TextField(choices=OPCIONES_RELACION)
