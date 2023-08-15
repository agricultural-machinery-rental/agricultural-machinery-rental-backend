from django.urls import reverse
from http import HTTPStatus

from core.fixtures import TestOrdersFixture
from orders.models import Reservation, ReservationStatus


class TestOrdersView(TestOrdersFixture):
    def test_get_all_orders(self):
        response = self.user_client.get(reverse("orders-list"))
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(Reservation.objects.all()))

    def test_get_one_order(self):
        response = self.user_client.get(
            reverse("orders-detail", kwargs={"pk": self.reservation1.id})
        )
        self.assertTrue(response.status_code, HTTPStatus.OK)

    def test_create_order(self):
        order_data = {
            "number": "2",
            "machinery": "2",
            "start_date": "2023-08-16T11:33:16.029352+03:00",
            "end_date": "2023-08-17T11:32:16.029352+03:00",
            "comment": "Нужно срочно!!",
        }
        response = self.user_client.post(
            reverse("orders-list"), data=order_data
        )
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Reservation.objects.filter(number="2", machinery_id=2).exists()
        )
        print(ReservationStatus.objects.all())
        self.assertTrue(
            ReservationStatus.objects.filter(
                status__name="0", reservation__machinery__id=2
            ).exists()
        )
