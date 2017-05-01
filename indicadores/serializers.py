from rest_framework import serializers

from estudios_socioeconomicos.utils import save_foreign_relationship

from .models import Periodo, Transaccion, Ingreso
from familias.models import Oficio


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

    def create(self):
        """ This function overides the default behaviour for creating
            an object through a serializer.
        """
        return Periodo.objects.create(**self.validated_data)

    def update(self):
        """ This function overides the default behaviour for updating
            an object through a serializer.
        """
        Periodo.objects.filter(pk=self.instance.pk).update(**self.validated_data)
        return Periodo.objects.get(pk=self.instance.pk)


class TransaccionSerializer(serializers.ModelSerializer):
    """ Serializer to represent a .models.Transaccion instance
        through a REST endpoint for the offline application
        to submit information.
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

            This serializer can be called from a familia create method.
            If we are dealing with familia Transactions of from a Tutor
            create method if we are dealing with Tutor Transactions.

            This serializer dependes on a .models.Familia
            object instance. Since we are dealing with
            nested created objects, the familia must be
            created first and passed as parameter to the
            created function.

            Finally a Periodo object is created from the data passed
            throught the serializer.
        """
        periodicidad = self.validated_data.pop('periodicidad')

        periodo = save_foreign_relationship(
            [periodicidad],
            PeriodoSerializer,
            Periodo)[0]

        self.validated_data['periodicidad'] = periodo
        self.validated_data['familia'] = familia

        return Transaccion.objects.create(**self.validated_data)

    def update(self):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            Updates a Transaccion object and the periodicidad nested object.
        """
        periodicidad = self.validated_data.pop('periodicidad')

        save_foreign_relationship(
            [periodicidad],
            PeriodoSerializer,
            Periodo)[0]

        Transaccion.objects.filter(pk=self.instance.pk).update(**self.validated_data)
        return Transaccion.objects.get(pk=self.instance.pk)


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
            'fecha',
            'tipo',
            'transaccion')

        extra_kwargs = {'id': {'read_only': False, 'required': False}}

    def create(self, tutor):
        """ This function overides the default behaviour for creating
            an object through a serializer.

            This object depends on a nested relation with transaccion
            therefore it creates the object before saving.
        """

        transaccion = self.validated_data.pop('transaccion')
        transaccion_instance = save_foreign_relationship(
            [transaccion],
            TransaccionSerializer,
            Transaccion,
            tutor.integrante.familia)

        self.validated_data['transaccion'] = transaccion_instance[0]
        self.validated_data['tutor'] = tutor
        return Ingreso.objects.create(**self.validated_data)

    def update(self):
        """ This function overides the default behaviour for updating
            an object through a serializer.

            Updates nested relashionship with transaccion and then updates
            local information.
        """

        transaccion = self.validated_data.pop('transaccion')
        save_foreign_relationship(
            [transaccion],
            TransaccionSerializer,
            Transaccion,
            self.instance.tutor.integrante.familia)

        Ingreso.objects.filter(pk=self.instance.pk).update(**self.validated_data)
        return Ingreso.objects.get(pk=self.instance.pk)
