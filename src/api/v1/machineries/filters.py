from django_filters import (
    ChoiceFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
    OrderingFilter,
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
    """Фильтры для экземпляров техники."""

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

    ordering = OrderingFilter(
        fields=(
            ("count_orders", "count_orders"),
            ("year_of_manufacture", "year_of_manufacture"),
            ("price_per_shift", "price_per_shift"),
            ("price_per_hour", "price_per_hour"),
        ),
        field_labels={
            "count_orders": "Количество заказов",
            "-count_orders": "Количество заказов (по убыванию)",
            "year_of_manufacture": "Год выпуска",
            "-year_of_manufacture": "Год выпуска (по убыванию)",
            "price_per_shift": "Цена за смену",
            "-price_per_shift": "Цена за смену (по убыванию)",
            "price_per_hour": "Цена за час",
            "-price_per_hour": "Цена за час (по убыванию)",
        },
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
            "year_of_manufacture",
            "count_orders",
        ]

    def filter_is_favorited(self, queryset, name, value):
        """Фильтрация по наличию в избранном."""

        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorite__user=user)
        return queryset
