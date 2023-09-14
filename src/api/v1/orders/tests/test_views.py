from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from http import HTTPStatus

from core.fixtures import TestOrdersFixture
from orders.models import Reservation


class TestOrdersView(TestOrdersFixture):
    def test_get_all_orders(self):
        response = self.user_client.get(reverse("orders-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(Reservation.objects.all()))

    def test_get_one_order(self):
        response = self.user_client.get(
            reverse("orders-detail", kwargs={"pk": self.reservation1.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_order(self):
        order_data = {
            "machinery": 2,
            "start_date": timezone.now() + timedelta(hours=12),
            "end_date": timezone.now() + timedelta(hours=13),
            "comment": "Нужно срочно!!",
        }
        response = self.user_client.post(
            reverse("orders-list"), data=order_data
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(
            Reservation.objects.filter(
                number=response.data["number"],
                machinery_id=response.data["machinery"],
            ).exists()
        )

    def test_existing_reservations(self):
        # Создаем заказ
        order_data = {
            "machinery": 2,
            "start_date": timezone.now() + timedelta(hours=10),
            "end_date": timezone.now() + timedelta(hours=20),
            "comment": "Нужно срочно!!",
        }
        answer = {"non_field_errors": ["Выбранные даты уже заняты."]}
        self.user_client.post(reverse("orders-list"), data=order_data)

        # Проверка: start_date нового заказа больше чем у созданного
        # end_date одинаковы
        order_data_2 = {
            "machinery": 2,
            "start_date": timezone.now() + timedelta(hours=11),
            "end_date": timezone.now() + timedelta(hours=20),
            "comment": "Нужно срочно!!",
        }
        response_2 = self.user_client.post(
            reverse("orders-list"), data=order_data_2
        )
        self.assertEqual(response_2.json(), answer)

        # Проверка: end_date нового заказа меньше чем у созданного
        # start_date одинаковы
        order_data_3 = {
            "machinery": 2,
            "start_date": timezone.now() + timedelta(hours=10),
            "end_date": timezone.now() + timedelta(hours=19),
            "comment": "Нужно срочно!!",
        }
        response_3 = self.user_client.post(
            reverse("orders-list"), data=order_data_3
        )
        self.assertEqual(response_3.json(), answer)

        # Проверка: end_date нового заказа меньше чем у созданного
        # и start_date нового заказа больше чем у созданного
        order_data_4 = {
            "machinery": 2,
            "start_date": timezone.now() + timedelta(hours=9),
            "end_date": timezone.now() + timedelta(hours=21),
            "comment": "Нужно срочно!!",
        }
        response_4 = self.user_client.post(
            reverse("orders-list"), data=order_data_4
        )
        self.assertEqual(response_4.json(), answer)

        # Проверка: создаем еще один заказ до созданного
        order_data_5 = {
            "machinery": 2,
            "start_date": timezone.now() + timedelta(hours=2),
            "end_date": timezone.now() + timedelta(hours=3),
            "comment": "Нужно срочно!!",
        }
        response_5 = self.user_client.post(
            reverse("orders-list"), data=order_data_5
        )
        self.assertTrue(
            Reservation.objects.filter(
                number=response_5.data["number"],
                machinery_id=response_5.data["machinery"],
            ).exists()
        )

        # Проверка: создаем еще один заказ после созданного первоначально
        order_data_6 = {
            "machinery": 2,
            "start_date": timezone.now() + timedelta(hours=30),
            "end_date": timezone.now() + timedelta(hours=40),
            "comment": "Нужно срочно!!",
        }
        response_6 = self.user_client.post(
            reverse("orders-list"), data=order_data_6
        )
        self.assertTrue(
            Reservation.objects.filter(
                number=response_6.data["number"],
                machinery_id=response_6.data["machinery"],
            ).exists()
        )

    def test_changing_reservation(self):
        # Проверка метода PATCH
        order_data = {
            "start_date": timezone.now() + timedelta(minutes=1),
            "end_date": timezone.now() + timedelta(hours=24),
            "comment": "Комментарий",
        }
        response = self.user_client.patch(
            reverse("orders-detail", kwargs={"pk": self.reservation1.id}),
            data=order_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data["comment"], order_data["comment"])
        # Проверка метода PUT
        order_data = {
            "machinery": 1,
            "start_date": timezone.now() + timedelta(minutes=1),
            "end_date": timezone.now() + timedelta(hours=24),
            "comment": "Другой комментарий",
        }
        response_2 = self.user_client.put(
            reverse("orders-detail", kwargs={"pk": self.reservation1.id}),
            data=order_data,
        )
        self.assertEqual(response_2.status_code, HTTPStatus.OK)
        self.assertEqual(response_2.data["comment"], order_data["comment"])

    def test_cancel_reservation(self):
        # отменяем резервацию
        cancel_reservation3 = self.user_client.post(
            reverse("orders-cancel", kwargs={"pk": self.reservation3.id})
        )
        self.assertEqual(
            cancel_reservation3.status_code, HTTPStatus.NO_CONTENT
        )

        # отмена уже отмененного резерва
        cancel_reservation3 = self.user_client.post(
            reverse("orders-cancel", kwargs={"pk": self.reservation3.id})
        )
        answer = {"message": "Такой резерв уже отменен!"}
        self.assertEqual(
            cancel_reservation3.status_code, HTTPStatus.BAD_REQUEST
        )
        self.assertEqual(cancel_reservation3.json(), answer)

        # отмена менее чем за 48 часов
        cancel_reservation4 = self.user_client.post(
            reverse("orders-cancel", kwargs={"pk": self.reservation4.id})
        )
        answer = {
            "message": (
                "Отмена невозможна! Осталось менее"
                " 48 часов до начала резервации."
            )
        }
        self.assertEqual(
            cancel_reservation4.status_code, HTTPStatus.BAD_REQUEST
        )
        self.assertEqual(cancel_reservation4.json(), answer)

    def test_count_orders_updates(self):
        machinery_before = self.user_client.get(
            reverse("machinery-detail", kwargs={"pk": 1})
        )

        order_data = {
            "machinery": 1,
            "start_date": timezone.now() + timedelta(hours=180),
            "end_date": timezone.now() + timedelta(hours=256),
            "comment": "Нужно срочно!!",
        }
        self.user_client.post(
            reverse("orders-list"),
            data=order_data,
        )

        machinery_after = self.user_client.get(
            reverse("machinery-detail", kwargs={"pk": 1})
        )

        self.assertEqual(
            machinery_before.data["count_orders"] + 1,
            machinery_after.data["count_orders"],
        )
