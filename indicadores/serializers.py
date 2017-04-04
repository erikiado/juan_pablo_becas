from rest_framework import serializers
from .models import Oficio, Periodo, Transaccion, Ingreso


class OficioSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Oficio instance
        through a REST endpoint for the offline application
        to submit information.
    """
    class Meta:
        model = Oficio
        fields = ('id', 'nombre')


class PeriodoSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Periodo instance
        through a REST endpoint for the offline application
        to submit information.
    """
    class Meta:
        model = Periodo
        fields = ('id', 'periodicidad', 'factor', 'multiplica')

        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class TransaccionSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Transaccion instance
        through a REST endpoint for the offline application
        to submit information.

        @TODO: Implement creating Ingreso from Transaccion
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
        """ This function overides the default behaviour for creating
            an object through a serializer.

            This serializer dependes on a .models.Familia
            object instance. Since we are dealing with
            nested created objects, the familia must be
            created first and passed as parameter to the
            created function.

            Finally a Periodo object os created from the data passed
            throught the serializer.
        """
        periodicidad = self.validated_data.pop('periodicidad')
        periodo = Periodo.objects.create(**periodicidad)
        self.validated_data['periodicidad'] = periodo
        self.validated_data['familia'] = familia

        return Transaccion.objects.create(**self.validated_data)

    def update(self):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            Updates a Transaccion object and the periodicidad nested object.
        """
        periodicidad = self.validated_data.pop('periodicidad')
        Periodo.objects.filter(pk=periodicidad['id']).update(**periodicidad)
        periodo = Periodo.objects.get(pk=periodicidad['id'])
        self.validated_data['periodicidad'] = periodo

        Transaccion.objects.filter(pk=self.instance.pk).update(**self.validated_data)
        return Periodo.objects.get(pk=self.instance.pk)


class IngresoSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Ingreso instance
        through a REST endpoint for the offline application
        to submit information.
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
        """ @TODO: This serializer is created through a Transaccion object.
        """
        return IngresoSerializer.objects.create(**self.validated_data)
