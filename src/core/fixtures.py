from datetime import datetime, timedelta
from rest_framework.test import APITestCase, APIClient

from machineries.models import Machinery, MachineryInfo
from orders.models import Reservation, Status
from users.models import User


class TestUserFixture(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User(
            email='vasya@vasya.ru', first_name='Vasya', password='vasya123'
        )
        cls.user.set_password('vasya123')
        cls.user.save()
        cls.user2 = User(
            email='petya@petya.ru', first_name='Petya', password='petya123'
        )
        cls.user2.set_password('petya123')
        cls.user2.save()
        cls.user3 = User(
            email='vanya@vanya.ru', first_name='Vanya', password='vanya123'
        )
        cls.user3.set_password('vanya123')
        cls.user3.save()

        cls.user_client = APIClient()
        cls.user_client.force_login(cls.user)
        cls.user2_client = APIClient()
        cls.user2_client.force_login(cls.user2)
        cls.user3_client = APIClient()
        cls.user3_client.force_login(cls.user3)


class TestMachinaryFixture(TestUserFixture, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.machinary1_info = MachineryInfo.objects.create(
            name="Трактор 1",
            category=1,
            description="Супер трактор",
            attachments_available=True,
            power_hp=150,
            payload_capacity_kg=1500
        )
        print(cls.machinary1_info)
        cls.machinary_1 = Machinery.objects.create(
            machinery=cls.machinary1_info,
            year_of_manufacture=2020,
            location='Здесь рядом',
            mileage=1000,
            delivery_distance_km=100,
            delivery_cost=150,
            rental_price=1000
        )
        cls.machinary2_info = MachineryInfo.objects.create(
            name="Комбайн 1",
            category=2,
            description="Супер комбайн",
            attachments_available=True,
            power_hp=750,
            payload_capacity_kg=1500
        )
        cls.machinary_2 = Machinery.objects.create(
            machinery=cls.machinary2_info,
            year_of_manufacture=2020,
            location='Тут недалеко',
            mileage=10000,
            delivery_distance_km=10,
            delivery_cost=250,
            rental_price=5000
        )


class TestOrdersFixture(TestMachinaryFixture, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.status_created = Status.objects.create(
            name=0,
            description='Заказ создан'
        )
        cls.status_confirmed = Status.objects.create(
            name=1,
            description='Заказ подтвержден'
        )
        cls.status_cancelled = Status.objects.create(
            name=2,
            description='Заказ отменен'
        )
        cls.status_at_work = Status.objects.create(
            name=3,
            description='В работе'
        )
        cls.status_finished = Status.objects.create(
            name=4,
            description='Заказ завершен'
        )
        cls.reservation1 = Reservation.objects.create(
            number="1",
            machinery=cls.machinary_1,
            renter=cls.user,
            start_date=datetime.now() + timedelta(minutes=1),
            end_date=datetime.now() + timedelta(hours=24)
        )
