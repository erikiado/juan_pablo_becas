from rest_framework import serializers

from .models import Retroalimentacion


class RetroalimentacionSerializer(serializers.ModelSerializer):
    """ Serializer to represent a Retroalimentacion object
        through a REST endpoint.
    """
    class Meta:
        model = Retroalimentacion
        fields = (
            'id',
            'usuario',
            'estudio',
            'fecha',
            'descripcion')

        read_only_fields = ('estudio', 'usuario')
