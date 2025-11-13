README — Sistema de Gestión de Aerolínea (EFI Final)

Autores: 
Mauricio Torres
Jeremias Herrrera
Arnold Grandberg

Materia: ingenieria de software

Año: 2025

 1. Descripción del Proyecto

Este proyecto implementa un sistema completo de gestión para una aerolínea, que incluye administración de:

Vuelos

Pasajeros

Aviones

Asientos

Boletos

Reservas

Autenticación mediante JWT

Reportes dinámicos

Panel administrativo

Documentación Swagger generada automáticamente

El sistema está desarrollado utilizando:

Django

Django REST Framework

Django Rest Framework SimpleJWT

drf-spectacular / drf-yasg para documentación

SQLite como base de datos por defecto

Incluye tanto la parte web tradicional (templates / views) como la API REST completa.

 2. Instalación y Ejecución del Proyecto
2.1. Clonar el repositorio
git clone https://github.com/MauriTorres9/Efi_aerolinea
cd Efi_aerolineas

2.2. Crear entorno virtual
python -m venv venv


Activar:

Windows

venv\Scripts\activate


Linux/Mac

source venv/bin/activate

2.3. Instalar dependencias
pip install -r requirements.txt


2.4. Crear y Aplicar migraciones}
python manage.py makemigrations
python manage.py migrate

2.5. Crear superusuario
python manage.py createsuperuser
cuando creas, se crea automaticamente como PAS(pasajero), lo que tenes que hacer es ir a la terminal shell y copiar este codigo

from django.contrib.auth import get_user_model
User = get_user_model()

u = User.objects.get(username="TU_USUARIO")   # reemplazalo por el nombre real
u.rol = "ADM"
u.is_staff = True
u.is_superuser = True
u.save()
print("Usuario actualizado a admin correctamente")

2.6. Ejecutar el servidor
python manage.py runserver

 3. Estructura principal del proyecto
efi2025/
├── aerolineas/
│   ├── api/
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   └── views.py
│   │
│   ├── repositories/
│   ├──services/
│   ├──templates/   
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── efi2025/
│   ├── urls.py
│   ├── settings.py
│ 
├── home/
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   └── templates/
│
│
└── manage.py

 4. Autenticación (JWT)
Login para obtener un token:
POST /api/token/

Body:

{
  "username": "admin",
  "password": "12345"
}

Renovar token:
POST /api/token/refresh/


 5. Documentación de la API

Swagger UI:
/api/docs/

Redoc:
/api/redoc/

Schema OpenAPI:
/api/schema/

 6. URLs Principales del Proyecto
6.1. URLs globales (efi2025/urls.py)
Ruta	Descripción
/admin/	Panel admin Django
/api/token/	Obtener JWT
/api/token/refresh/	Refrescar JWT
/api/	Endpoints principales de la API
/aerolineas/	Vistas web de la app
/	Home
/api/docs/	Swagger
/api/redoc/	Redoc
/api/schema/	Schema OpenAPI

 7. Endpoints de la API (DRF)

Archivo: aerolineas/api/urls.py

7.1 CRUD automáticos (ViewSets)

Todos estos endpoints permiten:

GET (lista y detalle)

POST

PUT / PATCH

DELETE

Vuelos
/api/vuelos/
/api/vuelos/<id>/

Pasajeros
/api/pasajeros/
/api/pasajeros/<id>/

Reservas
/api/reservas/
/api/reservas/<id>/

Aviones
/api/aviones/
/api/aviones/<id>/

Asientos
/api/asientos/
/api/asientos/<id>/

Boletos
/api/boletos/
/api/boletos/<id>/

 8. Endpoints de Reportes
Pasajeros por vuelo
GET /api/reportes/pasajeros/<vuelo_id>/

Reservas activas por pasajero
GET /api/reportes/reservas/<pasajero_id>/

Disponibilidad de asientos en un vuelo
GET /api/vuelos/<vuelo_pk>/asientos/disponibilidad/

 9. URLs del sitio web (templates)

Archivo: home/urls.py

Ruta	Descripción
/	Página principal
/login/	Inicio de sesión
/register/	Registrar usuario
/logout/	Cerrar sesión

 10. Cómo probar la API en Postman

Iniciar servidor

Crear superusuario

Obtener token en /api/token/

Enviar en Postman:

Headers:

Authorization: Bearer <tu_token>


Ejemplo:
GET → /api/vuelos/

 11. Base de Datos

 Se usa SQLite por defecto
 Migraciones incluidas
 Tablas generadas automáticamente por Django

 12. Mejoras implementadas (resumen técnico)

API 100% RESTful con ViewSets + Routers

Autenticación JWT

Serializers bien estructurados

Sistema de reportes personalizados

Documentación OpenAPI automática

Módulo web tradicional separado del API
