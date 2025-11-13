from rest_framework import serializers
from aerolineas.models import Vuelo, Pasajero, Reserva, Avion, Asiento, Boleto
from django.utils import timezone
import uuid

# ----- VUELOS -----
class VueloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vuelo
        fields = "__all__"


# ----- PASAJEROS -----
class PasajeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasajero
        fields = "__all__"


# ----- RESERVAS -----
class ReservaSerializer(serializers.ModelSerializer):
    # mostrar datos útiles
    pasajero = serializers.PrimaryKeyRelatedField(queryset=Pasajero.objects.all())
    vuelo = serializers.PrimaryKeyRelatedField(queryset=Vuelo.objects.all())
    asiento = serializers.PrimaryKeyRelatedField(queryset=Asiento.objects.all())

    class Meta:
        model = Reserva
        fields = ["id", "vuelo", "pasajero", "asiento", "estado", "fecha_reserva", "precio", "codigo_reserva"]
        read_only_fields = ("fecha_reserva",)

    def validate(self, data):
        """
        Validaciones:
        - El asiento pertenece al avión del vuelo.
        - El asiento no está ocupado por otra reserva 'confirmado' en el mismo vuelo.
        """
        vuelo = data.get("vuelo")
        asiento = data.get("asiento")
        estado = data.get("estado", "").lower()

        if asiento and vuelo:
            if asiento.avion_id != vuelo.avion_id:
                raise serializers.ValidationError("El asiento seleccionado no pertenece al avión asignado a ese vuelo.")

            # Si se está creando/confirmando una reserva comprobamos disponibilidad
            # Miramos reservas confirmadas que usan ese asiento en ese vuelo
            from aerolineas.models import Reserva as ReservaModel
            ocupada = ReservaModel.objects.filter(vuelo=vuelo, asiento=asiento, estado__iexact="confirmado").exists()
            if ocupada:
                raise serializers.ValidationError("El asiento ya está ocupado por otra reserva confirmada en este vuelo.")

        return data

    def create(self, validated_data):
        # Generar codigo_reserva si no viene
        if not validated_data.get("codigo_reserva"):
            validated_data["codigo_reserva"] = uuid.uuid4().hex[:8]

        # Fecha de reserva se maneja por defecto en el modelo
        reserva = super().create(validated_data)
        return reserva

    def update(self, instance, validated_data):
        # Si se actualiza a 'confirmado' verificar que no haya conflicto
        estado = validated_data.get("estado", instance.estado)
        if estado and estado.lower() == "confirmado":
            from aerolineas.models import Reserva as ReservaModel
            conflict = ReservaModel.objects.filter(vuelo=instance.vuelo, asiento=instance.asiento, estado__iexact="confirmado").exclude(pk=instance.pk).exists()
            if conflict:
                raise serializers.ValidationError("No se puede confirmar: el asiento ya está ocupado por otra reserva confirmada.")
        return super().update(instance, validated_data)


# ----- ASIENTOS DISPONIBILIDAD (serializador simple) -----
class AsientoDisponibilidadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    numero = serializers.CharField(allow_null=True)
    fila = serializers.IntegerField(allow_null=True)
    columna = serializers.IntegerField(allow_null=True)
    tipo = serializers.CharField(allow_null=True)
    disponible = serializers.BooleanField()


# ----- AVIONES -----
class AvionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avion
        fields = "__all__"


# ----- ASIENTOS -----
class AsientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asiento
        fields = "__all__"


# ----- BOLETOS -----
class BoletoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleto
        fields = "__all__"
