from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['comment_form'] = CommentForm()
        context['color_form'] = ProductColorForm(product=product)
        context['rating_form'] = RatingForm()
        context['comment_list'] = Comment.objects.filter(product=product,
                                                         status=Comment.Status.APPROVED)
        return context


class CommentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ['products.add_comment']
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        if next_url := self.request.GET.get('next'):
            return next_url
        return reverse_lazy('products:product-detail', kwargs={'pk': self.kwargs.get('product_id')})

    def form_valid(self, form):
        comment = form.save(commit=False)
        product = get_object_or_404(Product, pk=self.kwargs.get('product_id'))
        comment.product = product
        comment.customer = Customer.get_customer(user=self.request.user)
        comment.save()
        response = super().form_valid(form)
        messages.success(self.request, f"CommentCreateView")
        return response


class MyCommentsListView(PermissionRequiredMixin, ListView):
    permission_required = ['products.view_comment']
    model = Comment
    template_name = 'accounts/dashboard/dashboard.html'
    context_object_name = 'comment_list'
    extra_context = {
        'my_comment_list_section': 'active',
    }

    def get_queryset(self):
        return Comment.objects.filter(customer=Customer.get_customer(self.request.user))


class RatingCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ['products.add_rating']
    model = Rating
    form_class = RatingForm

    def test_func(self):
        customer = Customer.get_customer(user=self.request.user)
        store_product = get_object_or_404(StoreProduct, pk=self.kwargs.get('store_product_id'))
        return customer.has_ordered_product(store_product.product)

    def get_success_url(self):
        if next_url := self.request.GET.get('next'):
            return next_url
        return reverse_lazy('home')

    def form_valid(self, form):
        rating = form.save(commit=False)
        store_product = get_object_or_404(StoreProduct, pk=self.kwargs.get('store_product_id'))
        self.model.objects.update_or_create(
            store_product=store_product,
            customer=Customer.get_customer(user=self.request.user),
            defaults={'score': rating.score},
        )
        response = HttpResponseRedirect(self.get_success_url())
        messages.success(self.request, f"RatingCreateView")
        return response
