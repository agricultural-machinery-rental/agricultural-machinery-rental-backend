from datetime import datetime, timedelta

from core.fixtures import TestOrdersFixture
from orders.models import Reservation, ReservationStatus


class TestOrders(TestOrdersFixture):
    def test_order_creation(self):
        reservation = Reservation.objects.create(
            number="2",
            machinery=self.machinary_2,
            renter=self.user,
            start_date=datetime.now() + timedelta(minutes=15),
            end_date=datetime.now() + timedelta(hours=20)
        )
        self.assertTrue(Reservation.objects.filter(number=2).exists())
        self.assertTrue(
            ReservationStatus.objects.filter(
                reservation_id=reservation.id,
                status_id=self.status_created.id).exists()
        )
