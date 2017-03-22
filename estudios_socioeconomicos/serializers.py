from rest_framework import serializers

from .models import Pregunta, Subseccion, Seccion, OpcionRespuesta


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
