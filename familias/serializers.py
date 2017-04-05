from rest_framework import serializers

from estudios_socioeconomicos.utils import save_foreign_relationship
from administracion.models import Escuela
from administracion.serializers import EscuelaSerializer
from indicadores.serializers import TransaccionSerializer, IngresoSerializer
from indicadores.models import Transaccion, Ingreso

from .models import Familia, Comentario, Integrante, Alumno, Tutor


class ComentarioSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Comentario instance
        through a REST endpoint for the offline application
        to submit information.
    """

    class Meta:
        model = Comentario
        fields = ('id', 'fecha', 'texto')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}

    def create(self, family):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            This serializer dependes on a .models.Familia
            object instance. Since we are dealing with
            nested created objects, the familia must be
            created first and passed as parameter to the
            created function.
        """
        self.validated_data['familia'] = family
        return Comentario.objects.create(**self.validated_data)

    def update(self):
        """ This function overides the default behaviour for creating
            an object through a serializer since Nested Updates are
            not implemented by DRF.

            Returns
            -------
            Updated Instance of Comentario model.
        """
        Comentario.objects.filter(pk=self.instance.id).update(**self.validated_data)
        return Comentario.objects.get(pk=self.instance.id)


class AlumnoSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Alumno instance
        through a REST endpoint for the offline application
        to submit information.
    """
    escuela = EscuelaSerializer()

    class Meta:
        model = Alumno
        fields = ('id', 'activo', 'escuela')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}

    def create(self, integrante):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            This serializer dependes on a .models.Integrante
            object instance. Since we are dealing with
            nested created objects, the integrante must be
            created first and passed as parameter to the
            created function.
        """

        escuela = Escuela.objects.filter(nombre=self.validated_data['escuela']['nombre'])
        self.validated_data['escuela'] = escuela[0]
        self.validated_data['integrante'] = integrante
        return Alumno.objects.create(**self.validated_data)

    def update(self):
        """ This function overides the default behaviour for creating
            an object through a serializer since Nested Updates are
            not implemented by DRF.

            Returns
            -------
            Updated Instance of Alumno model.
        """
        escuela = Escuela.objects.filter(nombre=self.validated_data['escuela']['nombre'])
        self.validated_data['escuela'] = escuela[0]
        Alumno.objects.filter(pk=self.instance.pk).update(**self.validated_data)
        return Alumno.objects.get(pk=self.instance.pk)


class TutorSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Tutor instance
        through a REST endpoint for the offline application
        to submit information.
    """
    tutor_ingresos = IngresoSerializer(many=True, allow_null=True)

    class Meta:
        model = Tutor
        fields = ('id', 'relacion', 'tutor_ingresos')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}

    def create(self, integrante):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            This serializer dependes on a .models.Integrante
            object instance. Since we are dealing with
            nested created objects, the integrante must be
            created first and passed as parameter to the
            created function.
        """
        ingresos = self.validated_data.pop('tutor_ingresos', None)

        self.validated_data['integrante'] = integrante
        tutor = Tutor.objects.create(**self.validated_data)

        save_foreign_relationship(ingresos, IngresoSerializer, Ingreso, tutor)

        return tutor

    def update(self):
        """ This function overides the default behaviour for creating
            an object through a serializer since Nested Updates are
            not implemented by DRF.

            Returns
            -------
            Updated Instance of Tutor model.
        """
        ingresos = self.validated_data.pop('tutor_ingresos', None)
        save_foreign_relationship(ingresos, IngresoSerializer, Ingreso, self.instance)
        Tutor.objects.filter(pk=self.instance.pk).update(**self.validated_data)
        return Tutor.objects.get(pk=self.instance.pk)


class IntegranteSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Integrante instance
        through a REST endpoint for the offline application
        to submit information.

        DRF by default sets the id field to read_only. This
        makes it unaccesible in validated_data. When an instance
        is being updated we need to acces the id in the nested
        serializers so that we can send the actual instance to
        the update method.
    """
    alumno_integrante = AlumnoSerializer(allow_null=True)
    tutor_integrante = TutorSerializer(allow_null=True)

    class Meta:
        model = Integrante
        fields = (
            'id',
            'nombres',
            'apellidos',
            'telefono',
            'correo',
            'nivel_estudios',
            'fecha_de_nacimiento',
            'alumno_integrante',
            'tutor_integrante',
            'activo')

        extra_kwargs = {'id': {'read_only': False, 'required': False}}

    def create(self, family):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            This serializer's object dependes on a .models.Integrante
            object instance. Since we are dealing with nested
            created objects, the integrante must be created first
            and passed as parameter to the created function.

            The Integrante model has a two sepcialization which are
            indicated in the dictionary data as 'alumno_integrante'
            and 'tutor_integrante'. This means the Integrante is
            either a Tutor or an Alumno.

            This function removes that data from the validated_data
            dictionary, creates the Integrante and then creates the
            specialized instance of either Alumno or Tutor.

            Notes
            -----
            save_foreign_relationship does not create object on None
            object. Therefore if one of the specilizations is not
            indicated it is not created.
        """
        self.validated_data['familia'] = family

        alumno = self.validated_data.pop('alumno_integrante')
        tutor = self.validated_data.pop('tutor_integrante')
        integrante = Integrante.objects.create(**self.validated_data)

        save_foreign_relationship([alumno], AlumnoSerializer, Alumno, integrante)
        save_foreign_relationship([tutor], TutorSerializer, Alumno, integrante)

        return integrante

    def update(self):
        """ This function overides the default behaviour for creating
            an object through a serializer since Nested Updates are
            not implemented by DRF.

            Updates dependent object Alumno and Tutor.

            Returns
            -------
            Updated Instance of an Integrante model.
        """
        alumno = self.validated_data.pop('alumno_integrante')
        tutor = self.validated_data.pop('tutor_integrante')

        save_foreign_relationship([alumno], AlumnoSerializer, Alumno, self.instance)
        save_foreign_relationship([tutor], TutorSerializer, Tutor, self.instance)

        Integrante.objects.filter(pk=self.instance.pk).update(**self.validated_data)
        return Integrante.objects.filter(pk=self.instance.pk)


class FamiliaSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Familia instance
        through a REST endpoint for the offline application
        to submit information.
    """
    integrante_familia = IntegranteSerializer(many=True, allow_null=True)
    comentario_familia = ComentarioSerializer(many=True, allow_null=True)
    transacciones = TransaccionSerializer(many=True, allow_null=True)

    class Meta:
        model = Familia
        fields = (
            'id',
            'numero_hijos_diferentes_papas',
            'explicacion_solvencia',
            'estado_civil',
            'localidad',
            'comentario_familia',
            'integrante_familia',
            'transacciones')

        extra_kwargs = {'id': {'read_only': False, 'required': False}}

    def create(self):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            Django Rest Framework does not implement saving nested
            serializers.

            Creates a Family instance. There are objects related to
            the family that depend upon the creation of a family
            instance first. This are the Integrantes and Comentarios.

            We first remove all Integrante, Comentario and Transaccion
            from the validated data. We create the family and then we
            create this objects that require the family instance.
        """
        integrantes = self.validated_data.pop('integrante_familia')
        comentarios = self.validated_data.pop('comentario_familia')
        transacciones = self.validated_data.pop('transacciones')

        family_instance = Familia.objects.create(**self.validated_data)

        save_foreign_relationship(integrantes, IntegranteSerializer, Integrante, family_instance)
        save_foreign_relationship(comentarios, ComentarioSerializer, Comentario, family_instance)
        save_foreign_relationship(
            transacciones,
            TransaccionSerializer,
            Transaccion,
            family_instance)

        return family_instance

    def update(self):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            Django Rest Framework does not implement saving nested
            serializers.

            Updates a familia object and all other objects that
            depend on it. Since the offline client will submit a
            complete JSON of the study each time.

            When an offline client submits an update of a study,
            new information can be created. save_foreign_relationship
            looks for the id in the object. If there is no data it will
            create the object.

            Integrantes and Transacciones has a non-destructive way of disactivating.
            This is donde by changing the is_active field.

            Comentario does not have this field, so all comentario instances
            that were not sent by the offline application most be removed.
        """
        integrantes = self.validated_data.pop('integrante_familia')
        comentarios = self.validated_data.pop('comentario_familia')
        transacciones = self.validated_data.pop('transacciones')

        Comentario.objects.filter(
            familia=self.instance).exclude(
                id__in=[comment.get('id') for comment in comentarios]).delete()

        save_foreign_relationship(integrantes, IntegranteSerializer, Integrante, self.instance)
        save_foreign_relationship(comentarios, ComentarioSerializer, Comentario, self.instance)
        save_foreign_relationship(transacciones, TransaccionSerializer, Transaccion, self.instance)

        Familia.objects.filter(pk=self.instance.pk).update(**self.validated_data)

        return Familia.objects.get(pk=self.instance.pk)  # Returns updated instance
