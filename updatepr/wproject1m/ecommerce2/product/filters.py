
import django_filters

from product.models import Product


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['category',]

