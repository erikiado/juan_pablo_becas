from django.db.transaction import atomic
from rest_framework import serializers

from familias.serializers import FamiliaSerializer
from familias.models import Familia
from captura.serializers import RetroalimentacionSerializer

from .models import Pregunta, Subseccion, Seccion, OpcionRespuesta
from .models import Estudio, Respuesta, Foto
from .utils import save_foreign_relationship


class FotoSerializer(serializers.ModelSerializer):
    """ Serializer for using .models.Foto objects
        in REST endpoint

        Saves and image to media/ folder
    """
    class Meta:
        model = Foto
        fields = ('id', 'estudio', 'upload', 'file_name')


class OpcionRespuestaSerializer(serializers.ModelSerializer):
    """ Serializer for using .models.OpcionRespuesta objects
        in REST endpoint
    """
    class Meta:
        model = OpcionRespuesta
        fields = ('id', 'texto')


class PreguntaSerializer(serializers.ModelSerializer):
    """ Serializer for using .models.Pregunta objects
        in REST endpoint
    """
    opciones_pregunta = OpcionRespuestaSerializer(many=True)

    class Meta:
        model = Pregunta
        fields = (
            'id',
            'subseccion',
            'texto',
            'descripcion',
            'orden',
            'opciones_pregunta')


class SubseccionSerializer(serializers.ModelSerializer):
    """ Serializer for using .models.Subseccion objects
        in REST endpoint

        preguntas is retrieved and serialized through PreguntaSerializer
    """
    preguntas = PreguntaSerializer(many=True)

    class Meta:
        model = Subseccion
        fields = (
            'id',
            'seccion',
            'nombre',
            'numero',
            'seccion',
            'preguntas')


class SeccionSerializer(serializers.ModelSerializer):
    """ Serializer for using .models.Seccion objects
        in REST endpoint

        subsecciones uses SubseccionSerializer
    """
    subsecciones = SubseccionSerializer(many=True)

    class Meta:
        model = Seccion
        fields = (
            'id',
            'nombre',
            'numero',
            'subsecciones')


class RespuestaSerializer(serializers.ModelSerializer):
    """ Serializer for using .models.Respuesta objects
        in REST endpoint.
    """
    class Meta:
        model = Respuesta
        fields = (
            'estudio',
            'pregunta',
            'eleccion',
            'respuesta')

        read_only_fields = ('estudio', )


class EstudioSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Estudio instance
        through a REST endpoint for the offline application
        to submit information.
    """
    respuesta_estudio = RespuestaSerializer(many=True, allow_null=True)
    retroalimentacion_estudio = RetroalimentacionSerializer(
        many=True,
        allow_null=True,
        read_only=True)
    familia = FamiliaSerializer()

    class Meta:
        model = Estudio
        fields = (
            'id',
            'familia',
            'status',
            'capturista',
            'retroalimentacion_estudio',
            'respuesta_estudio')

        read_only_fields = ('id', 'capturista')

    @atomic
    def create(self, capturista):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            Django Rest Framework does not implement saving nested
            serializers.

            Estudio object depends on a Familia insance. This function
            first creates the familia, then creates the Estudio and
            finally creates all answers that depend on the Estudio.

            Notes
            -----
            Saves the Estudio instance using .save_base(raw=True). This
            is required because Estudio has a Trigger required for online
            client to create empy answers for any new study. The offline
            client does not require this functionality.

            save_foreign_relationship returns a list of created or updated
            objects. We just care about the first.

            The familia_data.pop('id', None) is just a defense mechanism in
            case somebody for some strange reason decides it's a good idea to
            send a study without an ID but a family with ID. We would just
            create e new family (family and estudio can only have 1 - 1 relashionship).
        """
        familia_data = self.validated_data.pop('familia')
        respuestas = self.validated_data.pop('respuesta_estudio')

        familia_data.pop('id', None)  # In the catastrofic case someone decides on sending

        family_instance = save_foreign_relationship([familia_data], FamiliaSerializer, Familia)

        if len(family_instance) != 1 or family_instance[0] is None:
            raise serializers.ValidationError('Family could not be created')

        self.validated_data['familia'] = family_instance[0]
        self.validated_data['capturista'] = capturista
        estudio = Estudio(**self.validated_data)

        if estudio.status == Estudio.BORRADOR or estudio.status == Estudio.REVISION:
            estudio.save_base(raw=True)  # Do not call Trigger (.models)
        else:
            raise serializers.ValidationError('Invalid status')

        for respuesta in respuestas:
            respuesta['estudio'] = estudio
            Respuesta.objects.create(**respuesta)

        return estudio

    @atomic
    def update(self):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            Django Rest Framework does not implement saving nested
            serializers.

            Updates an Estudio intance and all objects related to it
            when an offline clients submits an update.

            Deletes all existing answers and saves with the new
            information from the study. This is because offline client
            can delete, modify or add a given number of answers and will
            always send the all.
        """
        familia = self.validated_data.pop('familia')
        respuestas = self.validated_data.pop('respuesta_estudio')

        save_foreign_relationship([familia], FamiliaSerializer, Familia)

        if self.instance.status == Estudio.REVISION or self.instance.status == Estudio.BORRADOR \
                or self.instance.status == Estudio.RECHZADO:
            Estudio.objects.filter(pk=self.instance.pk).update(**self.validated_data)
        else:
            raise serializers.ValidationError('Invalid change of status')

        Respuesta.objects.filter(estudio=self.instance).delete()

        for respuesta in respuestas:
            respuesta['estudio'] = self.instance
            Respuesta.objects.create(**respuesta)

        return Estudio.objects.get(pk=self.instance.pk)
