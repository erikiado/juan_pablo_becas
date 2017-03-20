from rest_framework import serializers

from estudios_socioeconomicos.utils import save_foreign_relashionship

from .models import Familia, Comentario, Integrante, Alumno, Tutor


class ComentarioSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Comentario instance
        through a REST endpoint for the offline application
        to submit information.
    """
    class Meta:
        model = Comentario
        fields = ('id', 'fecha', 'texto')

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


class AlumnoSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Alumno instance
        through a REST endpoint for the offline application
        to submit information.
    """
    class Meta:
        model = Alumno
        fields = ('id', 'activo')

    def create(self, integrante):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            This serializer dependes on a .models.Integrante
            object instance. Since we are dealing with
            nested created objects, the integrante must be
            created first and passed as parameter to the
            created function.
        """
        self.validated_data['integrante'] = integrante
        return Alumno.objects.create(**self.validated_data)


class TutorSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Tutor instance
        through a REST endpoint for the offline application
        to submit information.
    """
    class Meta:
        model = Tutor
        fields = ('id', 'relacion')

    def create(self, integrante):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            This serializer dependes on a .models.Integrante
            object instance. Since we are dealing with
            nested created objects, the integrante must be
            created first and passed as parameter to the
            created function.
        """
        self.validated_data['integrante'] = integrante
        return Tutor.objects.create(**self.validated_data)


class IntegranteSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Integrante instance
        through a REST endpoint for the offline application
        to submit information.
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
            'tutor_integrante')

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
            save_foreign_relashionship does not create object on None
            object. Therefore if one of the specilizations is not
            indicated it is not created.
        """
        self.validated_data['familia'] = family

        alumno = self.validated_data.pop('alumno_integrante')
        tutor = self.validated_data.pop('tutor_integrante')

        integrante = Integrante.objects.create(**self.validated_data)

        save_foreign_relashionship([alumno], AlumnoSerializer, integrante)
        save_foreign_relashionship([tutor], TutorSerializer, integrante)

        return integrante


class FamiliaSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Familia instance
        through a REST endpoint for the offline application
        to submit information.
    """
    integrante_familia = IntegranteSerializer(many=True)
    comentario_familia = ComentarioSerializer(many=True)

    class Meta:
        model = Familia
        fields = (
            'id',
            'numero_hijos_diferentes_papas',
            'explicacion_solvencia',
            'estado_civil',
            'localidad',
            'comentario_familia',
            'integrante_familia',)

    def create(self):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            Django Rest Framework does not implement saving nested
            serializers.

            Creates a Family instance. There are objects related to
            the family that depend upon the creation of a family
            instance first. This are the Integrantes and Comentarios.

            We first remove all Integrante and comentario from the
            validated data. We create the family and then we create
            this objects that require the family instance.
        """
        integrantes = self.validated_data.pop('integrante_familia')
        comentarios = self.validated_data.pop('comentario_familia')

        family_instance = Familia.objects.create(**self.validated_data)

        save_foreign_relashionship(integrantes, IntegranteSerializer, family_instance)
        save_foreign_relashionship(comentarios, ComentarioSerializer, family_instance)

        return family_instance

    def update(self):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            Django Rest Framework does not implement saving nested
            serializers.

            Updates a familia object and all other objects that
            depend on it. Since the offline client will submit a
            complete JSON of the study each time. We first remove
            all dependant objets (Integrante and Comentario). Then
            we create them again. This is because the client can
            delete or create many of this objects locally but upload
            them after certain time.
        """
        integrantes = self.validated_data.pop('integrante_familia')
        comentarios = self.validated_data.pop('comentario_familia')

        for integrante in self.data.pop('integrante_familia'):
            Integrante.objects.get(pk=integrante.get('id')).delete()

        for commentario in self.data.pop('comentario_familia'):
            Comentario.objects.get(pk=commentario.get('id')).delete()

        save_foreign_relashionship(integrantes, IntegranteSerializer, self.instance)
        save_foreign_relashionship(comentarios, ComentarioSerializer, self.instance)

        Familia.objects.filter(pk=self.instance.pk).update(**self.validated_data)

        return Familia.objects.get(pk=self.instance.pk)  # Returns updated instance
