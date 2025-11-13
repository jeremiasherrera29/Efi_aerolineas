from rest_framework.permissions import BasePermission

class EsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'ADM'

class EsEmpleado(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'EMP'

class EsPasajero(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'PAS'
