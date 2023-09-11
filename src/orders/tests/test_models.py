from datetime import timedelta
from django.utils import timezone

from config.settings import PREFIX_ORDER_NUMBER
from core.fixtures import TestOrdersFixture
from orders.models import Reservation


class TestOrders(TestOrdersFixture):
    def test_order_creation(self):
        reservation = Reservation.objects.create(
            machinery=self.machinary_2,
            renter=self.user,
            start_date=timezone.now() + timedelta(minutes=15),
            end_date=timezone.now() + timedelta(hours=20),
        )
        self.assertTrue(
            Reservation.objects.filter(number=reservation.number).exists()
        )

        year = timezone.now().strftime("%Y")
        self.assertTrue(reservation.number.startswith("AG" + year))
        self.assertTrue(reservation.number[len("AG" + year) :].isdigit())

        expected_number = f"{PREFIX_ORDER_NUMBER}{year}000005"
        self.assertEqual(reservation.number, expected_number)
