import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method='filter_category')
    colors = django_filters.CharFilter(method='filter_colors')
    sizes = django_filters.CharFilter(
        field_name='state', lookup_expr='icontains')
    min_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'colors', 'max_price', 'min_price', 'sizes']

    def filter_category(self, queryset, name, value):
        if value:
            category = value.split(',')
            return queryset.filter(category__name__in=category)
        return queryset

    def filter_colors(self, queryset, name, value):
        if value:
            colors = value.split(',')
            return queryset.filter(colors__name__in=colors)
        return queryset
