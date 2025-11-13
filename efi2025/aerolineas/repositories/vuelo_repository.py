# aerolineas/repositories/vuelo_repository.py
from aerolineas.models import Vuelo

class VueloRepository:
    @staticmethod
    def obtener_todos(filtros=None):
        queryset = Vuelo.objects.all()

        if filtros:
            if filtros.get("origen"):
                queryset = queryset.filter(origen__icontains=filtros["origen"])
            if filtros.get("destino"):
                queryset = queryset.filter(destino__icontains=filtros["destino"])
            if filtros.get("fecha"):
                queryset = queryset.filter(fecha_salida=filtros["fecha"])

        return queryset.order_by("fecha_salida")
