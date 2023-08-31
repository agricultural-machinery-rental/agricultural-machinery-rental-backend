from datetime import timedelta
from django.utils import timezone

from core.fixtures import TestOrdersFixture
from orders.models import Reservation


class TestOrders(TestOrdersFixture):
    def test_order_creation(self):
        Reservation.objects.create(
            number="2",
            machinery=self.machinary_2,
            renter=self.user,
            start_date=timezone.now() + timedelta(minutes=15),
            end_date=timezone.now() + timedelta(hours=20),
        )
        self.assertTrue(Reservation.objects.filter(number=2).exists())
