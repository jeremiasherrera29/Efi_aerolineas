from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from datetime import datetime
import uuid
from aerolineas.services.vuelo_service import VueloService

from aerolineas.models import Vuelo, Pasajero, Reserva, Avion, Asiento, Boleto
from .serializers import (
    VueloSerializer, PasajeroSerializer, ReservaSerializer,
    AvionSerializer, AsientoSerializer, BoletoSerializer, AsientoDisponibilidadSerializer
)

#     PERMISOS PERSONALIZADOS

class IsAdmin(permissions.BasePermission):
    """Permite acceso solo a usuarios con rol Administrador (ADM)."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "rol", None) == "ADM"


class IsEmpleado(permissions.BasePermission):
    """Permite acceso a Empleados y Administradores."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "rol", None) in ["EMP", "ADM"]


class IsPasajero(permissions.BasePermission):
    """Permite acceso a Pasajeros autenticados."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "rol", None) == "PAS"


#           VUELOS


class VueloViewSet(viewsets.ModelViewSet):
    queryset = Vuelo.objects.all()
    serializer_class = VueloSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        vuelos = VueloService.listar_vuelos(request.query_params)

        page = self.paginate_queryset(vuelos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(vuelos, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        """Filtrado por origen, destino o fecha."""
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


#          PASAJEROS

class PasajeroViewSet(viewsets.ModelViewSet):
    queryset = Pasajero.objects.all()
    serializer_class = PasajeroSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsEmpleado()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=["get"])
    def reservas(self, request, pk=None):
        pasajero = self.get_object()
        reservas = Reserva.objects.filter(pasajero=pasajero)
        return Response(ReservaSerializer(reservas, many=True).data)


#          RESERVAS

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsEmpleado()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """Los pasajeros solo ven sus propias reservas."""
        user = self.request.user
        if getattr(user, "rol", None) == "PAS":
            return Reserva.objects.filter(pasajero__email=user.email)
        return Reserva.objects.all()

    @action(detail=True, methods=["post"])
    def confirmar(self, request, pk=None):
        reserva = self.get_object()

        if reserva.estado.lower() == "confirmado":
            return Response({"error": "La reserva ya está confirmada."}, status=400)

        reserva.estado = "confirmado"
        reserva.save()

        boleto_existente = Boleto.objects.filter(reserva=reserva).first()
        if not boleto_existente:
            Boleto.objects.create(
                reserva=reserva,
                codigo_barra=str(uuid.uuid4())[:8],
                fecha_emision=datetime.now(),
                estado="emitido"
            )

        return Response({"status": "Reserva confirmada y boleto generado"}, status=200)

    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        reserva = self.get_object()

        if reserva.estado.lower() == "cancelado":
            return Response({"error": "La reserva ya está cancelada."}, status=400)

        reserva.estado = "cancelado"
        reserva.save()

        boleto = Boleto.objects.filter(reserva=reserva).first()
        if boleto:
            boleto.estado = "cancelado"
            boleto.save()

        return Response({"status": "Reserva cancelada y boleto anulado"}, status=200)


#           AVIONES

class AvionViewSet(viewsets.ModelViewSet):
    queryset = Avion.objects.all()
    serializer_class = AvionSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


#           ASIENTOS

class AsientoViewSet(viewsets.ModelViewSet):
    queryset = Asiento.objects.all()
    serializer_class = AsientoSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


#           BOLETOS


class BoletoViewSet(viewsets.ModelViewSet):
    queryset = Boleto.objects.all()
    serializer_class = BoletoSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsEmpleado()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=["get"], url_path="codigo/(?P<codigo>[^/.]+)")
    def buscar_por_codigo(self, request, codigo=None):
        boleto = Boleto.objects.filter(codigo_barra=codigo).first()
        if not boleto:
            return Response({"error": "Boleto no encontrado"}, status=404)
        serializer = self.get_serializer(boleto)
        return Response(serializer.data)


#           REPORTES

class ReportePasajerosPorVuelo(APIView):
    """Solo los administradores pueden ver pasajeros por vuelo."""
    permission_classes = [IsAdmin]

    def get(self, request, vuelo_id):
        reservas = Reserva.objects.filter(vuelo_id=vuelo_id, estado="confirmado")
        pasajeros = [r.pasajero for r in reservas]
        return Response(PasajeroSerializer(pasajeros, many=True).data)


class ReporteReservasActivas(APIView):
    """Cualquier usuario autenticado puede ver sus reservas activas."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pasajero_id):
        reservas = Reserva.objects.filter(pasajero_id=pasajero_id, estado="confirmado")
        return Response(ReservaSerializer(reservas, many=True).data)


#   DISPONIBILIDAD DE ASIENTOS


class AsientoDisponibilidadAPIView(APIView):
    """
    GET /api/v1/vuelos/<vuelo_pk>/asientos/disponibilidad/
    Retorna todos los asientos del avión del vuelo y si están ocupados por una Reserva confirmada.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, vuelo_pk):
        vuelo = get_object_or_404(Vuelo, pk=vuelo_pk)
        asientos = Asiento.objects.filter(avion=vuelo.avion).order_by('fila', 'columna')
        reservas_ocupadas = Reserva.objects.filter(vuelo=vuelo, estado="confirmado").values_list('asiento_id', flat=True)

        data = []
        for a in asientos:
            disponible = a.pk not in reservas_ocupadas
            data.append({
                "id": a.pk,
                "numero": a.numero,
                "fila": a.fila,
                "columna": a.columna,
                "tipo": a.tipo,
                "disponible": disponible,
            })

        serializer = AsientoDisponibilidadSerializer(data, many=True)
        return Response({"vuelo": vuelo.pk, "asientos": serializer.data}, status=status.HTTP_200_OK)
