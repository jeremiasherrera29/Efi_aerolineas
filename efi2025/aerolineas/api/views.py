from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from aerolineas.models import Vuelo, Pasajero, Reserva, Avion, Asiento, Boleto
from .serializers import (
    VueloSerializer, PasajeroSerializer, ReservaSerializer,
    AvionSerializer, AsientoSerializer, BoletoSerializer
)

# ----- PERMISOS PERSONALIZADOS -----
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "rol", None) == "ADM"

class IsEmpleado(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "rol", None) in ["EMP", "ADM"]

# ----- VIEWSETS -----
class VueloViewSet(viewsets.ModelViewSet):
    queryset = Vuelo.objects.all()
    serializer_class = VueloSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        origen = self.request.query_params.get("origen")
        destino = self.request.query_params.get("destino")
        fecha = self.request.query_params.get("fecha")
        vuelos = Vuelo.objects.all()
        if origen:
            vuelos = vuelos.filter(origen__icontains=origen)
        if destino:
            vuelos = vuelos.filter(destino__icontains=destino)
        if fecha:
            vuelos = vuelos.filter(fecha_salida=fecha)
        return vuelos

class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"])
    def reservas(self, request, pk=None):
        pasajero = self.get_object()
        reservas = Reserva.objects.filter(pasajero=pasajero)
        return Response(ReservaSerializer(reservas, many=True).data)

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"])
    def confirmar(self, request, pk=None):
        reserva = self.get_object()
        reserva.estado = "CONFIRMADA"
        reserva.save()
        return Response({"status": "Reserva confirmada"})

    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        reserva.estado = "CANCELADA"
        reserva.save()
        return Response({"status": "Reserva cancelada"})

class AvionViewSet(viewsets.ModelViewSet):
    queryset = Avion.objects.all()
    serializer_class = AvionSerializer
    permission_classes = [permissions.IsAuthenticated]

class AsientoViewSet(viewsets.ModelViewSet):
    queryset = Asiento.objects.all()
    serializer_class = AsientoSerializer
    permission_classes = [permissions.IsAuthenticated]

class BoletoViewSet(viewsets.ModelViewSet):
    queryset = Boleto.objects.all()
    serializer_class = BoletoSerializer
    permission_classes = [IsEmpleado]

# ----- REPORTES -----

class ReportePasajerosPorVuelo(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, vuelo_id):
        reservas = Reserva.objects.filter(vuelo_id=vuelo_id, estado="CONFIRMADA")
        pasajeros = [r.pasajero for r in reservas]
        return Response(PasajeroSerializer(pasajeros, many=True).data)

class ReporteReservasActivas(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pasajero_id):
        reservas = Reserva.objects.filter(pasajero_id=pasajero_id, estado="CONFIRMADA")
        return Response(ReservaSerializer(reservas, many=True).data)
