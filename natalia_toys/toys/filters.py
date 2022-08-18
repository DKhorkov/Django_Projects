import django_filters

from .models import Toy


class ToysFilter(django_filters.FilterSet):
    """Создание системы фильтрации игрушек по названию и цене.
    https://django-filter.readthedocs.io/en/stable/index.html"""

    choices = (('ascending', 'По возрастанию цены'), ('descending', 'По убыванию цены'))
    ordering = django_filters.ChoiceFilter(label='Сортировка по цене', choices=choices, method='filter_by_order')

    class Meta:
        model = Toy
        # Только имеющиеся названия, описания и цены в диапазоне:
        fields = {'title': ['icontains'], 'price': ['gte', 'lte'], 'description': ['icontains']}

    def filter_by_order(self, queryset, name, users_choice):
        """Фильтрация всех игрушек в возрастающем или уменьшающем порядке по цене."""
        expression = 'price' if users_choice == 'ascending' else '-price'
        return queryset.order_by(expression)
