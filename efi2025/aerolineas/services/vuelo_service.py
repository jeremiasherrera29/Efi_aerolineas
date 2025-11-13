from aerolineas.repositories.vuelo_repository import VueloRepository

class VueloService:
    @staticmethod
    def listar_vuelos(params):
        filtros = {
            "origen": params.get("origen"),
            "destino": params.get("destino"),
            "fecha": params.get("fecha"),
        }

        return VueloRepository.obtener_todos(filtros)
