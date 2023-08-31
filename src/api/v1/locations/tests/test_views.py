from django.urls import reverse
from http import HTTPStatus

from core.fixtures import TestLocationFixture
from locations.models import Location, Region


class TestMachineryView(TestLocationFixture):
    def test_get_locations_list(self):
        response = self.user2_client.get(reverse("locations-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), len(Location.objects.all()))

    def test_locations_filter(self):
        response_1 = self.user_client.get(
            reverse("locations-list") + f"?title={self.location_1.title}"
        )
        self.assertEqual(
            len(response_1.data),
            len(
                Location.objects.filter(
                    title=self.location_1.title
                )
            ),
        )
        response_2 = self.user_client.get(
            reverse("locations-list") + f"?region__title={self.region_1.title}"
        )
        self.assertEqual(
            len(response_2.data),
            len(
                Location.objects.filter(
                    region__title=self.region_1.title
                )
            ),
        )

    def test_get_regions_list(self):
        response = self.user2_client.get(reverse("regions-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), len(Region.objects.all()))

    def test_regions_filter(self):
        response = self.user_client.get(
            reverse("locations-list") + f"?title={self.region_2.title}"
        )
        self.assertEqual(
            len(response.data),
            len(
                Location.objects.filter(
                    title=self.region_2.title
                )
            ),
        )
