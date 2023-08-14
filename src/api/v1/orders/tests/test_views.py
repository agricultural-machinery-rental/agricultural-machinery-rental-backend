from django.urls import reverse
from http import HTTPStatus

from core.fixtures import TestOrdersFixture
from orders.models import Reservation


class TestOrdersView(TestOrdersFixture):
    def test_get_all_orders(self):
        response = self.user_client.get(reverse("orders-list"))
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(Reservation.objects.all()))

    def test_get_one_order(self):
        response = self.user_client.get(
            reverse(
                "orders-detail",
                kwargs={"pk": self.reservation1.id}
            )
        )
        self.assertTrue(response.status_code, HTTPStatus.OK)
