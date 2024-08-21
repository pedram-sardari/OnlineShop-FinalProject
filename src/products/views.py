from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.db.models import Min, F, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView

from customers.models import Customer
from .forms import CommentForm, RatingForm, ProductColorForm
from .models import Product, StoreProduct, Comment, Rating


class StoreProductListView(ListView):
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


class StoreProductDetailView(DetailView):
    model = StoreProduct
    template_name = 'products/store_product_detail.html'
    context_object_name = 'store_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['color_form'] = ProductColorForm(product=self.get_object().product)
        context['rating_form'] = RatingForm()
        context['comment_list'] = Comment.objects.filter(product=self.get_object().product,
                                                         status=Comment.Status.APPROVED)
        customer = Customer.get_customer(user=self.request.user)
        if customer:
            context['can_rate'] = (customer.has_ordered_store_product(self.get_object())
                                   and not customer.has_rated_store_product(self.get_object()))
        return context


class CommentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ['products.add_comment']
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('products:store-product-detail', kwargs={'pk': self.kwargs.get('store_product_id')})

    def form_valid(self, form):
        comment = form.save(commit=False)
        store_product = get_object_or_404(StoreProduct, pk=self.kwargs.get('store_product_id'))
        comment.product = store_product.product
        comment.customer = Customer.get_customer(user=self.request.user)
        comment.save()
        return super().form_valid(form)


class RatingCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ['products.add_rating']
    model = Rating
    form_class = RatingForm

    def test_func(self):
        customer = Customer.get_customer(user=self.request.user)
        store_product = get_object_or_404(StoreProduct, pk=self.kwargs.get('store_product_id'))
        return (customer.has_ordered_store_product(store_product)
                and not customer.has_ordered_customer(store_product))

    def get_success_url(self):
        return reverse_lazy('products:store-product-detail', kwargs={'pk': self.kwargs.get('store_product_id')})

    def form_valid(self, form):
        rating = form.save(commit=False)
        store_product = get_object_or_404(StoreProduct, pk=self.kwargs.get('store_product_id'))
        self.model.objects.update_or_create(
            product=store_product.product,
            customer=Customer.get_customer(user=self.request.user),
            defaults={'score': rating.score},
        )
        return HttpResponseRedirect(self.get_success_url())
