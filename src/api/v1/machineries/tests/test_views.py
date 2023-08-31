from django.urls import reverse
from http import HTTPStatus

from core.fixtures import TestMachinaryFixture
from machineries.models import (
    Machinery,
    MachineryBrandname,
    MachineryInfo,
    WorkType,
)


class TestWorkTypeView(TestMachinaryFixture):
    def test_get_work_types_list(self):
        response = self.user2_client.get(reverse("work_type-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), len(WorkType.objects.all()))


class TestMachineryView(TestMachinaryFixture):
    def test_get_machineries_list(self):
        response = self.user2_client.get(reverse("machinery-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), len(Machinery.objects.all()))

    def test_machineries_filter(self):
        response_1 = self.user_client.get(
            reverse("machinery-list") + f"?mark={self.brand_1.brand}"
        )
        self.assertEqual(
            len(response_1.data),
            len(
                Machinery.objects.filter(
                    machinery__mark__brand=self.brand_1.brand
                )
            ),
        )

        response_2 = self.user_client.get(
            reverse("machinery-list") + f"?work_type={self.work_type_1.slug}"
        )
        self.assertEqual(
            len(response_2.data),
            len(
                Machinery.objects.filter(
                    machinery__work_type__slug=self.work_type_1.slug
                )
            ),
        )

        response_3 = self.user_client.get(
            reverse("machinery-list") + "?category=1"
        )
        self.assertEqual(
            len(response_3.data),
            len(Machinery.objects.filter(machinery__category=1)),
        )

        response_4 = self.user_client.get(
            reverse("machinery-list") + f"?name={self.machinary1_info.name}"
        )
        self.assertEqual(
            len(response_4.data),
            len(
                Machinery.objects.filter(
                    machinery__name=self.machinary1_info.name
                )
            ),
        )

        response_5 = self.user_client.get(
            (
                reverse("machinery-list")
                + "?price_per_hour_min=500.00"
                + "&price_per_hour_max=1100.00"
            )
        )
        self.assertEqual(
            len(response_5.data),
            len(
                Machinery.objects.filter(
                    price_per_hour__gte=500.00,
                    price_per_hour__lte=1100.00,
                )
            ),
        )

        response_6 = self.user_client.get(
            (
                reverse("machinery-list")
                + "?price_per_shift_min=10000.00"
                + "&price_per_shift_max=21000.00"
            )
        )
        self.assertEqual(
            len(response_6.data),
            len(
                Machinery.objects.filter(
                    price_per_shift__gte=10000.00,
                    price_per_shift__lte=21000.00,
                )
            ),
        )

        response_7 = self.user_client.get(
            (reverse("machinery-list") + f"?location={self.location_1.title}")
        )
        self.assertEqual(
            len(response_7.data),
            len(
                Machinery.objects.filter(location__title=self.location_1.title)
            ),
        )

        response_8 = self.user_client.get(
            (reverse("machinery-list") + f"?region={self.region_1.title}")
        )
        self.assertEqual(
            len(response_8.data),
            len(
                Machinery.objects.filter(
                    location__region__title=self.region_1.title
                )
            ),
        )


class TestMachineryBrandnameView(TestMachinaryFixture):
    def test_get_brands_list(self):
        response = self.user2_client.get(reverse("brands-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            len(response.data), len(MachineryBrandname.objects.all())
        )


class TestMachineryInfoView(TestMachinaryFixture):
    def test_get_models_list(self):
        response = self.user2_client.get(reverse("models-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), len(MachineryInfo.objects.all()))
