from rest_framework import serializers

from .models import Escuela


class EscuelaSerializer(serializers.ModelSerializer):
    """ Serializer para el modelo de Escuela.
    """
    class Meta:
        model = Escuela
        fields = ('id', 'nombre')
