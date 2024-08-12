from django.db.models import Min, F, Count, Sum
from django.shortcuts import render
from django.views.generic import ListView

from .models import Product, StoreProduct


class ProductListView(ListView):
    model = StoreProduct
    template_name = 'website/index.html'
    context_object_name = 'store_product_list'
    sort_by = {
        'best_seller': '-order_count',
        'highest_rating': '-product__rating_avg',
        'most_expensive': '-price',
        'cheapest': 'price'
    }
    ordering_kwargs = 'sort'
    paginate_by = 3
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        ordering = self.request.GET.get(self.ordering_kwargs)
        context['ordering'] = f"{self.ordering_kwargs}={ordering if ordering in self.sort_by else 'best_seller'}"
        return context

    def get_ordering(self):
        return self.sort_by.get(self.request.GET.get(self.ordering_kwargs), '-order_count')

    def get_queryset(self):
        qs = self.model.objects.filter(
            inventory__gt=0
        ).annotate(
            min_price=Min('product__store_products__price')
        ).filter(
            price=F('min_price')
        ).annotate(
            order_count=Sum('order_items__quantity')
        ).order_by(
            self.get_ordering()
        ).distinct()
        print('2' * 50)
        print(repr(qs.values('order_count')))
        print('1' * 50)
        return qs


