from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient

from machineries.models import (
    Machinery,
    MachineryBrandname,
    MachineryInfo,
    WorkType,
)
from orders.models import Reservation
from users.models import User


class TestUserFixture(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User(
            email="vasya@vasya.ru",
            first_name="Vasya",
            last_name="Vasya",
            phone_number="+71110000000",
            password="vasya123",
        )
        cls.user.set_password("vasya123")
        cls.user.save()
        cls.user2 = User(
            email="petya@petya.ru",
            first_name="Petya",
            password="petya123",
            phone_number="+71110000001",
            last_name="Petya",
        )
        cls.user2.set_password("petya123")
        cls.user2.save()
        cls.user3 = User(
            email="vanya@vanya.ru",
            first_name="Vanya",
            last_name="Vanya",
            phone_number="+71110000002",
            password="vanya123",
        )
        cls.user3.set_password("vanya123")
        cls.user3.save()

        cls.user_client = APIClient()
        cls.user_client.force_authenticate(cls.user)
        cls.user2_client = APIClient()
        cls.user2_client.force_authenticate(cls.user2)
        cls.user3_client = APIClient()
        cls.user3_client.force_authenticate(cls.user3)


class TestMachinaryFixture(TestUserFixture, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.work_type_1 = WorkType.objects.create(title="Сеять", slug="seyat")
        cls.work_type_2 = WorkType.objects.create(title="Жать", slug="jat")
        cls.work_type_3 = WorkType.objects.create(title="Копать", slug="copat")
        cls.brand_1 = MachineryBrandname.objects.create(brand="JCB")
        cls.brand_2 = MachineryBrandname.objects.create(brand="Komatsu")
        cls.machinary1_info = MachineryInfo.objects.create(
            name="Трактор 1",
            mark=cls.brand_1,
            category=1,
            description="Супер трактор",
            attachments_available=True,
            power_hp=150,
            payload_capacity_kg=1500,
        )
        cls.machinary1_info.work_type.add(cls.work_type_3)
        cls.machinary_1 = Machinery.objects.create(
            machinery=cls.machinary1_info,
            year_of_manufacture=2020,
            location="Здесь рядом",
            mileage=1000,
            delivery_distance_km=100,
            delivery_cost=150,
            rental_price=1000,
        )
        cls.machinary2_info = MachineryInfo.objects.create(
            name="Комбайн 1",
            category=2,
            mark=cls.brand_2,
            description="Супер комбайн",
            attachments_available=True,
            power_hp=750,
            payload_capacity_kg=1500,
        )
        cls.machinary2_info.work_type.add(cls.work_type_1, cls.work_type_2)
        cls.machinary_2 = Machinery.objects.create(
            machinery=cls.machinary2_info,
            year_of_manufacture=2020,
            location="Тут недалеко",
            mileage=10000,
            delivery_distance_km=10,
            delivery_cost=250,
            rental_price=5000,
        )


class TestOrdersFixture(TestMachinaryFixture, APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.reservation1 = Reservation.objects.create(
            number="1",
            machinery=cls.machinary_1,
            renter=cls.user,
            start_date=timezone.now() + timedelta(minutes=1),
            end_date=timezone.now() + timedelta(hours=24),
        )
        cls.reservation2 = Reservation.objects.create(
            number="10",
            machinery=cls.machinary_2,
            renter=cls.user,
            start_date="2123-08-26T11:33:16.029352+03:00",
            end_date="2123-08-27T11:32:16.029352+03:00",
        )
        cls.reservation3 = Reservation.objects.create(
            number="10",
            machinery=cls.machinary_2,
            renter=cls.user,
            start_date="2123-08-18T11:33:16.029352+03:00",
            end_date="2123-08-18T12:32:16.029352+03:00",
        )
        cls.reservation4 = Reservation.objects.create(
            number="11",
            machinery=cls.machinary_1,
            renter=cls.user,
            start_date=timezone.now() + timedelta(hours=47),
            end_date=timezone.now() + timedelta(hours=96),
        )