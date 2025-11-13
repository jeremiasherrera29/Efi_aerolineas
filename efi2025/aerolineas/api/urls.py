from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VueloViewSet, PasajeroViewSet, ReservaViewSet,
    AvionViewSet, AsientoViewSet, BoletoViewSet,
    ReportePasajerosPorVuelo, ReporteReservasActivas, AsientoDisponibilidadAPIView
)

router = DefaultRouter()
router.register("vuelos", VueloViewSet)
router.register("pasajeros", PasajeroViewSet)
router.register("reservas", ReservaViewSet)
router.register("aviones", AvionViewSet)
router.register("asientos", AsientoViewSet)
router.register("boletos", BoletoViewSet)

urlpatterns = [
    path("", include(router.urls)), 
    path("reportes/pasajeros/<int:vuelo_id>/", ReportePasajerosPorVuelo.as_view()),
    path("reportes/reservas/<int:pasajero_id>/", ReporteReservasActivas.as_view()),
    path("vuelos/<int:vuelo_pk>/asientos/disponibilidad/", AsientoDisponibilidadAPIView.as_view(), name="asiento-disponibilidad"),
    path("reportes/pasajeros/<int:vuelo_id>/", ReportePasajerosPorVuelo.as_view()),
    path("reportes/reservas/<int:pasajero_id>/", ReporteReservasActivas.as_view()),
]
