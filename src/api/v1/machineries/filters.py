from django_filters import (
    CharFilter,
    ChoiceFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
    RangeFilter,
)

from core.choices_classes import Category
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
    location = CharFilter(field_name="location", lookup_expr="icontains")
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
            "machinery__work_type",
            "machinery__category",
            "machinery__name",
            "location",
            "price_per_hour",
            "machinery__mark__brand",
            "price_per_shift",
        ]
