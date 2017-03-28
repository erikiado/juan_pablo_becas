from rest_framework import serializers
from .models import Escuela

class EscuelaSerializer(serializers.ModelSerializer):
	""" Serializer for Escuelas that are part of JPII organization.
    """
    class Meta:
        model = Escuela
        fields = ('id', 'nombre')
