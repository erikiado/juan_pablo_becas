from datetime import datetime
from django.db import models
from core.validators import PHONE_REGEX
from administracion.models import Escuela


class Oficio(models.Model):
    """ This model stores the list of all possible jobs.

    This list of jobs stores the information related to a family
    member, this model is used directly for the presentation and
    creation of the indicators related to the jobs of tutors.

    Attributes:
    -----------
    nombre : TextField
        This field stores the name of a job.
    """

    nombre = models.CharField(max_length=200)

    def __str__(self):
        """ This returns the name of the Oficio

        """
        return '{}'.format(self.nombre)


class Sacramento(models.Model):
    """ This model stores a list of sacraments of the Catholic Church.

    This list of sacraments stores the information related to a family
    member, this model is used directly for the presentation and
    creation of the indicators related to the sacraments of each family members.

    Attributes:
    -----------
    nombre : TextField
        This field stores the name of the sacrament.
    """

    nombre = models.CharField(max_length=200)

    def __str__(self):
        """ This returns the name of the Sacramento

        """
        return '{}'.format(self.nombre)


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
    OPCIONES_BANIO : tuple(tuple())
        This is a field that stores the list of options to be stored in the banio field.
    OPCIONES_SANITARIAS : tuple(tuple())
        This is a field that stores the list of options to be stored in the sanitarios field.
    numero_hijos_diferentes_papas : IntegerField
        The content of this field needs to be clarified with the stakeholder, whether this
        is the number of unique parents, the children of a mother have, or just the total
        number of children.
    nombre_familiar: CharField
        This field will be used as an alias for the capturista to easily find the family.
    direccion: TextField
        This field should be filed with the home address for the family.
    explicacion_solvencia : TextField
        This field should be filled in their net mensual income is negative. It serves as an
        explanation on how the family deals with the deficit.
    estado_civil : CharField
        This field stores the information regarding the legal relationship status of the
        parents in a family.
    escuela : TextField
        This field stores an optional value for the school, in case that the integrante is
        a student.
    localidad : CharField
        This field stores the town in which a family resides.
    banio : CharField
        This field stores the information related to the shower instalation in a house.
    sanitarios : CharField
        This field stores the information related to the W.C instalation in a house.

    TODO:
    -----
    - Clarify the contents of the number_hijos_diferentes_papas field
    """

    OPCION_ESTADO_SOLTERO = 'soltero'
    OPCION_ESTADO_VIUDO = 'viudo'
    OPCION_ESTADO_UNION_LIBRE = 'union_libre'
    OPCION_ESTADO_CASADO_CIVIL = 'casado_civil'
    OPCION_ESTADO_CASADO_IGLESIA = 'casado_iglesia'
    OPCION_ESTADO_VUELTO_CASAR = 'vuelto_a_casar'

    OPCIONES_ESTADO_CIVIL = ((OPCION_ESTADO_SOLTERO, 'Soltero'),
                             (OPCION_ESTADO_VIUDO, 'Viudo'),
                             (OPCION_ESTADO_UNION_LIBRE, 'Unión Libre'),
                             (OPCION_ESTADO_CASADO_CIVIL, 'Casado-Civil'),
                             (OPCION_ESTADO_CASADO_IGLESIA, 'Casado-Iglesia'),
                             (OPCION_ESTADO_VUELTO_CASAR, 'Divorciado Vuelto a Casar'))

    OPCION_LOCALIDAD_JURICA = 'poblado_jurica'
    OPCION_LOCALIDAD_NABO = 'nabo'
    OPCION_LOCALIDAD_SALITRE = 'salitre'
    OPCION_LOCALIDAD_CAMPANA = 'la_campana'
    OPCION_LOCALIDAD_OTRO = 'otro'
    OPCIONES_LOCALIDAD = ((OPCION_LOCALIDAD_JURICA, 'Poblado Juríca'),
                          (OPCION_LOCALIDAD_NABO, 'Nabo'),
                          (OPCION_LOCALIDAD_SALITRE, 'Salitre'),
                          (OPCION_LOCALIDAD_CAMPANA, 'La Campana'),
                          (OPCION_LOCALIDAD_OTRO, 'Otro'))

    OPCION_REGADERA = 'Regadera'
    OPCION_JICARA = 'Jicarasos'
    OPCION_OTRO = 'Otro'
    OPCIONES_BANIO = ((OPCION_REGADERA, 'Regadera'),
                      (OPCION_JICARA, 'Jicarasos'),
                      (OPCION_OTRO, 'Otro'))

    OPCION_ESCUSADO = 'Escusado'
    OPCION_LETRINA = 'Letrina'
    OPCIONES_SANITARIAS = ((OPCION_ESCUSADO, 'Escusado'),
                           (OPCION_LETRINA, 'Letrina'),
                           (OPCION_OTRO, 'Otro'))

    numero_hijos_diferentes_papas = models.IntegerField()
    nombre_familiar = models.CharField(max_length=300)
    explicacion_solvencia = models.TextField(blank=True)
    direccion = models.TextField(blank=True)
    estado_civil = models.CharField(max_length=100,
                                    choices=OPCIONES_ESTADO_CIVIL)
    localidad = models.CharField(max_length=100,
                                 choices=OPCIONES_LOCALIDAD)
    banio = models.CharField(max_length=100,
                             choices=OPCIONES_BANIO,
                             verbose_name='Tipo de instalación de baño',
                             blank=True)
    sanitarios = models.CharField(max_length=100,
                                  choices=OPCIONES_SANITARIAS,
                                  verbose_name='Tipo de instalación sanitaria',
                                  blank=True)

    def __str__(self):
        """ Prints the apellido of one of the students of the family,
        in case the family has no related students the legend
        "Aún no se crean alumnos en el estudio" will appear.
        """
        return self.nombre_familiar


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

    familia = models.ForeignKey(Familia, related_name='comentario_familia')
    fecha = models.DateTimeField(null=True, blank=True, auto_now_add=True)
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
    escuela: CharField
        This attribute stores the school of a family member who is student.
    fecha_de_nacimiento : DateField
        Store the date of birth of a family member.
    activo: BooleanField
        This attribute stores information about the involvment of a family member
        with the family itself.

    TODO:
    -----
    - Implement foreign key relationship with oficio.
    """
    OPCION_ESTUDIOS_NINGUNO = 'ninguno'
    OPCION_ESTUDIOS_1 = '1_grado'
    OPCION_ESTUDIOS_2 = '2_grado'
    OPCION_ESTUDIOS_3 = '3_grado'
    OPCION_ESTUDIOS_4 = '4_grado'
    OPCION_ESTUDIOS_5 = '5_grado'
    OPCION_ESTUDIOS_6 = '6_grado'
    OPCION_ESTUDIOS_7 = '7_grado'
    OPCION_ESTUDIOS_8 = '8_grado'
    OPCION_ESTUDIOS_9 = '9_grado'
    OPCION_ESTUDIOS_10 = '10_grado'
    OPCION_ESTUDIOS_11 = '11_grado'
    OPCION_ESTUDIOS_12 = '12_grado'
    OPCION_ESTUDIOS_UNIVERSIDAD = 'universidad'
    OPCION_ESTUDIOS_MAESTRIA = 'maestria'
    OPCION_ESTUDIOS_DOCTORADO = 'doctorado'
    OPCION_ESTUDIOS_PREESCOLAR_1 = 'kinder_1'
    OPCION_ESTUDIOS_PREESCOLAR_2 = 'kinder_2'
    OPCION_ESTUDIOS_PREESCOLAR_3 = 'kinder_3'
    OPCIONES_NIVEL_ESTUDIOS = ((OPCION_ESTUDIOS_NINGUNO, 'Ninguno'),
                               (OPCION_ESTUDIOS_PREESCOLAR_1, 'Primero de Preescolar'),
                               (OPCION_ESTUDIOS_PREESCOLAR_2, 'Segundo de Preescolar'),
                               (OPCION_ESTUDIOS_PREESCOLAR_3, 'Tercero de Preescolar'),
                               (OPCION_ESTUDIOS_1, 'Primero de Primaria'),
                               (OPCION_ESTUDIOS_2, 'Segundo de Primaria'),
                               (OPCION_ESTUDIOS_3, 'Tercero de Primaria'),
                               (OPCION_ESTUDIOS_4, 'Cuarto de Primaria'),
                               (OPCION_ESTUDIOS_5, 'Quinto de Primaria'),
                               (OPCION_ESTUDIOS_6, 'Sexto de Primaria'),
                               (OPCION_ESTUDIOS_7, 'Primero de Secundaria'),
                               (OPCION_ESTUDIOS_8, 'Segundo de Secundaria'),
                               (OPCION_ESTUDIOS_9, 'Tercero de Secundaria'),
                               (OPCION_ESTUDIOS_10, 'Primero de Preparatoria'),
                               (OPCION_ESTUDIOS_11, 'Segundo de Preparatoria'),
                               (OPCION_ESTUDIOS_12, 'Tercero de Preparatoria'),
                               (OPCION_ESTUDIOS_UNIVERSIDAD, 'Universidad'),
                               (OPCION_ESTUDIOS_MAESTRIA, 'Maestría'),
                               (OPCION_ESTUDIOS_DOCTORADO, 'Doctorado'))
    familia = models.ForeignKey(Familia, related_name='integrante_familia')
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    oficio = models.ForeignKey(Oficio, null=True, blank=True)
    telefono = models.CharField(validators=[PHONE_REGEX], blank=True, max_length=16)
    correo = models.EmailField(blank=True)
    offline_id = models.TextField(blank=True)
    especificacion_oficio = models.TextField(blank=True)
    especificacion_estudio = models.TextField(blank=True)
    nivel_estudios = models.CharField(max_length=200,
                                      choices=OPCIONES_NIVEL_ESTUDIOS)
    fecha_de_nacimiento = models.DateField()
    sacramentos = models.ManyToManyField(Sacramento, blank=True)
    sacramentos_text = \
        'Sacramentos que le falten… bautizo, comunion, confirmación, matrimonio iglesia'
    sacramentos_faltantes = models.TextField(blank=True,
                                             verbose_name=sacramentos_text)
    hist = '¿Asiste o asistió a terapia por alguna situación de AA, psicología, psiquiatría, etc.?'
    historial_terapia = models.TextField(blank=True, verbose_name=hist)
    escuela = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=True)
    rol = models.CharField(max_length=150, verbose_name='Relación en la familia')

    def age(self):
        """ Returns the age of an instance of integrante

        """
        return int((datetime.now().date() - self.fecha_de_nacimiento).days / 365.25)

    def __str__(self):
        """ Returns the concatenation of nombres and apellidos.

        The concatenation of nombres and apellidos generates the full name of
        a family member.
        """
        return '{nombres} {apellidos}'.format(nombres=self.nombres, apellidos=self.apellidos)


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
    ciclo_escolar : CharField
        This field stores the schoolar cycle (i.e. 2017 - 2018) in which the student
        was enrolled.
    entry_status : CharField
        This field stores the information about whether the studen is new or is
        re-entry

    TODO: activate the ManyToOne with Escuela once the model is declared in the
    administracion app.
    """

    OPCIONES_CICLOS_ESCOLARES = [
        (str(x), "%d - %d" % (x, x + 1)) for x in map(lambda x: x, range(2010, 2051))
    ]

    OPCION_REINGRESO = 'reingreso'
    OPCION_NUEVO = 'nuevo'
    OPCIONES_ESTATUS_INGRESO = (
        (OPCION_REINGRESO, 'Reingreso'),
        (OPCION_NUEVO, 'Nuevo')
    )

    integrante = models.OneToOneField(Integrante, related_name='alumno_integrante')
    activo = models.BooleanField(default=True)
    numero_sae = models.CharField(max_length=30)
    escuela = models.ForeignKey(Escuela, related_name='escuela_alumno')
    ciclo_escolar = models.CharField(max_length=6,
                                     choices=OPCIONES_CICLOS_ESCOLARES,
                                     default='2017')
    estatus_ingreso = models.CharField(max_length=10,
                                       choices=OPCIONES_ESTATUS_INGRESO,
                                       default=OPCION_REINGRESO)

    def __str__(self):
        """ Returns the name of the student

        This return value is taken directly from the Integrante class.
        """
        return '{}'.format(self.integrante)


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
    OPCION_RELACION_MADRE = 'madre'
    OPCION_RELACION_PADRE = 'padre'
    OPCION_RELACION_TUTOR = 'tutor'
    OPCIONES_RELACION = ((OPCION_RELACION_MADRE, 'Madre'),
                         (OPCION_RELACION_PADRE, 'Padre'),
                         (OPCION_RELACION_TUTOR, 'Tutor'))

    integrante = models.OneToOneField(Integrante, related_name='tutor_integrante')
    relacion = models.CharField(max_length=75, choices=OPCIONES_RELACION)

    def __str__(self):
        """ Return the name of the tutor.

        The return value is taken direclty form the Integrante class.
        """
        return '{}'.format(self.integrante)
