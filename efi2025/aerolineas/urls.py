from django.urls import path
from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import (
    VueloList, VueloDetail, VueloDelete, VueloCreate,
    PasajeroList, PasajeroDetail, PasajeroDelete, PasajeroCreate, 
    ReservaList, ReservaDelete, ReservaCreate,ReservaDetail,
    BoletoList, BoletoDelete, BoletoCreate,BuscarBoletoView,BoletoDetail,
    UsuarioList, UsuarioDelete, UsuarioCreate, UsuarioUpdate,
    AvionList, AvionDetail, AvionDelete, AvionCreate,
    AsientoList, AsientoDetail, AsientoDelete, AsientoCreate,
    RegisterView    
)

urlpatterns = [
    # Vuelos   
    path('vuelos/', VueloList.as_view(), name='vuelos_list'),
    path('vuelos/<int:vuelo_id>/', VueloDetail.as_view(), name='vuelos_detail'),
    path('vuelos/<int:vuelo_id>/eliminar/', VueloDelete.as_view(), name='vuelos_delete'),
    path('vuelos/crear/', VueloCreate.as_view(), name='vuelos_create'),

    # Pasajeros
    path('pasajeros/', PasajeroList.as_view(), name='pasajeros_list'),
    path('pasajeros/<int:pasajero_id>/', PasajeroDetail.as_view(), name='pasajeros_detail'),
    path('pasajeros/<int:pasajero_id>/eliminar/', PasajeroDelete.as_view(), name='pasajeros_delete'),
    path('pasajeros/crear/', PasajeroCreate.as_view(), name='pasajeros_create'),
    # Historial de vuelos
    path('pasajeros/<int:pasajero_id>/historial/', views.HistorialVuelosPasajero.as_view(), name='pasajeros_historial'),


    # Reservas
    path('reservas/', ReservaList.as_view(), name='reservas_list'),
    path('reservas/crear/', ReservaCreate.as_view(), name='reservas_create'),
    path('reservas/<int:reserva_id>/', ReservaDetail.as_view(), name='reservas_detail'),
    path('reservas/<int:reserva_id>/eliminar/', ReservaDelete.as_view(), name='reservas_delete'),


    # Boletos
    path('boletos/', BoletoList.as_view(), name='boletos_list'),
    path('boletos/<int:boleto_id>/eliminar/', BoletoDelete.as_view(), name='boletos_delete'),
    path('boletos/crear/', BoletoCreate.as_view(), name='boletos_create'),
    path("boletos/buscar", BuscarBoletoView.as_view(), name="buscar_boleto"),
    path('boletos/<int:pk>/', views.BoletoDetail.as_view(), name='boletos_detail'),

    # Usuarios
    path('usuarios/', UsuarioList.as_view(), name='usuarios_list'),
    path('usuarios/<int:usuario_id>/eliminar/', UsuarioDelete.as_view(), name='usuarios_delete'),
    path('usuarios/crear/', UsuarioCreate.as_view(), name='usuarios_create'),
    path('usuarios/<int:usuario_id>/editar/', UsuarioUpdate.as_view(), name='usuarios_update'),

    # Aviones
    path('aviones/', AvionList.as_view(), name='aviones_list'),
    path('aviones/<int:avion_id>/', AvionDetail.as_view(), name='aviones_detail'),
    path('aviones/<int:avion_id>/eliminar/', AvionDelete.as_view(), name='aviones_delete'),
    path('aviones/crear/', AvionCreate.as_view(), name='aviones_create'),

    # Asientos
    path('asientos/', views.AsientoList.as_view(), name='asientos_list'),
    path('asientos/<int:asiento_id>/', views.AsientoDetail.as_view(), name='asientos_detail'),
    path('asientos/create/', views.AsientoCreate.as_view(), name='asientos_create'),
    path('asientos/<int:asiento_id>/delete/', views.AsientoDelete.as_view(), name='asientos_delete'),

    path("register/", RegisterView.as_view(), name="register"),

    # Disponibilidad y reservas
    path('vuelos/<int:vuelo_id>/asientos/', views.disponibilidad_asientos, name='disponibilidad_asientos'),
    path('vuelos/<int:vuelo_id>/asientos/<int:asiento_id>/reservar/', views.reservar_asiento, name='reservar_asiento'),

    path('reportes/pasajeros/<int:vuelo_id>/', views.reporte_pasajeros_por_vuelo, name='reporte_pasajeros_por_vuelo'),
]

schema_view = get_schema_view(
    openapi.Info(
        title="API Aerolínea",
        default_version="v1",
        description="Documentación de la API del Sistema de Gestión de Aerolínea",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path("api/", include("aerolineas.api.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
]