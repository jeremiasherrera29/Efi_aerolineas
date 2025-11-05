from rest_framework import serializers
from aerolineas.models import Vuelo, Pasajero, Reserva, Avion, Asiento, Boleto

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
    pasajero = PasajeroSerializer(read_only=True)
    vuelo = VueloSerializer(read_only=True)

    class Meta:
        model = Reserva
        fields = "__all__"

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
