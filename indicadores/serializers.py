from rest_framework import serializers
from .models import Oficio, Periodo, Transaccion, Ingreso


class OficioSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Oficio
        fields = ('id', 'nombre')


class PeriodoSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Periodo
        fields = ('id', 'periodicidad', 'factor', 'multiplica')

        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class TransaccionSerializer(serializers.ModelSerializer):
    """
    """
    periodicidad = PeriodoSerializer()

    class Meta:
        model = Transaccion
        fields = (
            'id',
            'activo',
            'monto',
            'periodicidad',
            'observacion',
            'es_ingreso')

        extra_kwargs = {'id': {'read_only': False, 'required': False}}

    def create(self, familia):
        """
        """
        periodicidad = self.validated_data.pop('periodicidad')
        periodo = Periodo.objects.create(**periodicidad)
        self.validated_data['periodicidad'] = periodo
        self.validated_data['familia'] = familia

        return Transaccion.objects.create(**self.validated_data)

    def update(self):
        """
        """
        periodicidad = self.validated_data.pop('periodicidad')
        Periodo.objects.filter(pk=periodicidad['id']).update(**periodicidad)
        periodo = Periodo.objects.get(pk=periodicidad['id'])
        self.validated_data['periodicidad'] = periodo

        Transaccion.objects.filter(pk=self.instance.pk).update(**self.validated_data)
        return Periodo.objects.get(pk=self.instance.pk)


class IngresoSerializer(serializers.ModelSerializer):
    """
    """
    transaccion = TransaccionSerializer()

    class Meta:
        model = Ingreso
        fields = (
            'id',
            'transaccion',
            'fecha',
            'tipo',
            'tutor')

    def create(self, tutor):
        """
        """
        return IngresoSerializer.objects.create(**self.validated_data)
