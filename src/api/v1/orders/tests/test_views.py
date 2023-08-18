from django.urls import reverse
from http import HTTPStatus

from core.fixtures import TestOrdersFixture
from orders.models import Reservation, ReservationStatus


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
            "number": "2",
            "machinery": 2,
            "start_date": "2123-08-16T11:33:16.029352+03:00",
            "end_date": "2123-08-17T11:32:16.029352+03:00",
            "comment": "Нужно срочно!!",
        }
        response = self.user_client.post(
            reverse("orders-list"), data=order_data
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(
            Reservation.objects.filter(number="2", machinery_id=2).exists()
        )
        self.assertTrue(
            ReservationStatus.objects.filter(
                status__name="0", reservation__machinery__id=2
            ).exists()
        )

    def test_existing_reservations(self):
        # Создаем заказ
        order_data = {
            "number": "2",
            "machinery": 2,
            "start_date": "2123-08-14T11:33:16.029352+03:00",
            "end_date": "2123-08-20T11:32:16.029352+03:00",
            "comment": "Нужно срочно!!",
        }
        answer = {"non_field_errors": ["Выбранные даты уже заняты."]}
        self.user_client.post(reverse("orders-list"), data=order_data)

        # Проверка: start_date нового заказа больше чем у созданного
        # end_date одинаковы
        order_data_2 = {
            "number": "3",
            "machinery": 2,
            "start_date": "2123-07-16T11:33:16.029352+03:00",
            "end_date": "2123-08-20T11:32:16.029352+03:00",
            "comment": "Нужно срочно!!",
        }
        response_2 = self.user_client.post(
            reverse("orders-list"), data=order_data_2
        )
        self.assertEqual(response_2.json(), answer)

        # Проверка: end_date нового заказа меньше чем у созданного
        # start_date одинаковы
        order_data_3 = {
            "number": "4",
            "machinery": 2,
            "start_date": "2123-08-14T11:33:16.029352+03:00",
            "end_date": "2123-08-21T11:32:16.029352+03:00",
            "comment": "Нужно срочно!!",
        }
        response_3 = self.user_client.post(
            reverse("orders-list"), data=order_data_3
        )
        self.assertEqual(response_3.json(), answer)

        # Проверка: end_date нового заказа меньше чем у созданного
        # и start_date нового заказа больше чем у созданного
        order_data_4 = {
            "number": "5",
            "machinery": 2,
            "start_date": "2123-08-15T11:33:16.029352+03:00",
            "end_date": "2123-08-19T11:32:16.029352+03:00",
            "comment": "Нужно срочно!!",
        }
        response_4 = self.user_client.post(
            reverse("orders-list"), data=order_data_4
        )
        self.assertEqual(response_4.json(), answer)

        # Проверка: создаем еще один заказ до созданного
        order_data_5 = {
            "number": "6",
            "machinery": 2,
            "start_date": "2123-08-10T11:33:16.029352+03:00",
            "end_date": "2123-08-13T11:32:16.029352+03:00",
            "comment": "Нужно срочно!!",
        }
        response_5 = self.user_client.post(
            reverse("orders-list"), data=order_data_5
        )
        self.assertEqual(response_5.json(), order_data_5)

        # Проверка: создаем еще один заказ после созданного первоначально
        order_data_6 = {
            "number": "7",
            "machinery": 2,
            "start_date": "2123-08-21T11:33:16.029352+03:00",
            "end_date": "2123-08-22T11:32:16.029352+03:00",
            "comment": "Нужно срочно!!",
        }
        response_6 = self.user_client.post(
            reverse("orders-list"), data=order_data_6
        )
        self.assertEqual(response_6.json(), order_data_6)

    def test_changing_reservation(self):
        # Проверка метода PATCH
        order_data = {
            "number": "10",
            "start_date": "2123-08-21T11:33:16.029352+03:00",
            "end_date": "2123-08-22T11:32:16.029352+03:00",
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
            "number": "10",
            "machinery": 1,
            "start_date": "2123-08-21T11:33:16.029352+03:00",
            "end_date": "2123-08-22T11:32:16.029352+03:00",
            "comment": "Другой комментарий",
        }
        response_2 = self.user_client.put(
            reverse("orders-detail", kwargs={"pk": self.reservation1.id}),
            data=order_data,
        )
        self.assertEqual(response_2.status_code, HTTPStatus.OK)
        self.assertEqual(response_2.data["comment"], order_data["comment"])
