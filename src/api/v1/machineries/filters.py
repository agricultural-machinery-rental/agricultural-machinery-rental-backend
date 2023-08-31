from django_filters import (
    ChoiceFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
    RangeFilter,
)

from core.choices_classes import Category
from locations.models import Location, Region
from machineries.models import (
    Machinery,
    MachineryBrandname,
    MachineryInfo,
    WorkType,
)


class MachineryFilter(FilterSet):
    mark = ModelMultipleChoiceFilter(
        field_name="machinery__mark__brand",
        to_field_name="brand",
        queryset=MachineryBrandname.objects.all(),
    )
    work_type = ModelMultipleChoiceFilter(
        field_name="machinery__work_type__slug",
        to_field_name="slug",
        queryset=WorkType.objects.all(),
    )
    location = ModelMultipleChoiceFilter(
        field_name="location__title",
        to_field_name="title",
        queryset=Location.objects.all(),
    )
    region = ModelMultipleChoiceFilter(
        field_name="location__region__title",
        to_field_name="title",
        queryset=Region.objects.all(),
    )
    price_per_hour = RangeFilter(field_name="price_per_hour")
    price_per_shift = RangeFilter(field_name="price_per_shift")
    name = ModelMultipleChoiceFilter(
        field_name="machinery__name",
        to_field_name="name",
        queryset=MachineryInfo.objects.all(),
    )
    category = ChoiceFilter(
        field_name="machinery__category", choices=Category.choices
    )

    class Meta:
        model = Machinery
        fields = [
            "work_type",
            "category",
            "name",
            "location",
            "region",
            "price_per_hour",
            "mark",
            "price_per_shift",
        ]
