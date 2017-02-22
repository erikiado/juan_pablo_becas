from django.db import models


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

    numero_hijos_differentes_papas : IntegerField
        The content of this field needs to be clarified with the stake holder, wether this
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
    egresos tables are created.d

    - Clarify the contents of the number_hijos_differentes_papas field

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

    numero_hijos_differentes_papas = models.IntegerField(default=0)
    explicacion_solvencia = models.TextField()
    estado_civil = models.TextField(choices=OPCIONES_ESTADO_CIVIL)
    localidad = models.TextField(choices=OPCIONES_LOCALIDAD)
