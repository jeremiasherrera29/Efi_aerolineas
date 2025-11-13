from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Avion, Vuelo, Asiento, Reserva

User = get_user_model()

class AsientoDisponibilidadTests(APITestCase):
    def setUp(self):
        # crear usuario (usando create_user para que password sea hashed)
        self.user = User.objects.create_user(username="testuser", password="pass1234", rol="EMP")
        # crear avion
        self.avion = Avion.objects.create(modelo="Boeing 737", capacidad=100, filas=10, columnas=10)
        # crear vuelo
        from datetime import datetime, timedelta
        ahora = datetime.now()
        self.vuelo = Vuelo.objects.create(
            avion=self.avion,
            origen="A",
            destino="B",
            fecha_salida=ahora,
            fecha_llegada=ahora + timedelta(hours=2),
            duracion=timedelta(hours=2),
            estado="PRG",
            precio_base=100.00
        )
        # crear asientos
        self.as1 = Asiento.objects.create(avion=self.avion, numero="1A", fila=1, columna=1, tipo="ECO", estado="Disponible")
        self.as2 = Asiento.objects.create(avion=self.avion, numero="1B", fila=1, columna=2, tipo="ECO", estado="Disponible")
        # crear reserva que ocupa as1
        self.reserva = Reserva.objects.create(vuelo=self.vuelo, pasajero=None, asiento=self.as1, estado="confirmado", precio=100.00, codigo_reserva="ABC123")

        # obtener token JWT
        url = reverse("token_obtain_pair")
        resp = self.client.post(url, {"username": "testuser", "password": "pass1234"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        token = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_disponibilidad(self):
        url = reverse("asiento-disponibilidad", kwargs={"vuelo_pk": self.vuelo.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        ids = {a["id"]: a for a in data["asientos"]}
        self.assertFalse(ids[self.as1.pk]["disponible"])
        self.assertTrue(ids[self.as2.pk]["disponible"])
