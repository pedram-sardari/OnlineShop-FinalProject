from django.db.models import Sum, F, Min
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from products.models import StoreProduct
from vendors.models import Store
from website.paginations import MyPagination
from .serializer import StoreProductVendorsSerializer, StoreSerializer, StoreProductSerializer


class StoreProductVendorListAPIView(ListAPIView):
    serializer_class = StoreProductVendorsSerializer
    queryset = StoreProduct.objects.all()

    def list(self, request, *args, **kwargs):
        product_color_id = self.request.query_params.get('product_color_id')
        product_name = self.request.query_params.get('product_name')
        print('*' * 50, product_color_id)
        print('*' * 50, product_name)
        if product_color_id:
            qs = self.queryset.filter(product__name=product_name, product_color_id=product_color_id).order_by('price')
        else:
            qs = self.queryset.filter(product__name=product_name).order_by('price')
        serializer = self.get_serializer_class()(qs, many=True)
        return Response(serializer.data)


class StoreListAPIView(ListAPIView):
    """
     name, description, address, product_count, rate
    """
    serializer_class = StoreSerializer
    queryset = Store.objects.all().annotate(orders_count=Sum('store_products__order_items__quantity'))
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['id', 'created_at', 'orders_count', 'rating_avg']
    ordering = ['id']


class StoreProductListAPIView(ListAPIView):
    serializer_class = StoreProductSerializer
    queryset = StoreProduct.objects.annotate(order_count=Sum('order_items__quantity'))
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['store__slug']
    search_fields = ['product__name']
    ordering_fields = ['order_count', 'price', 'product__rating_avg']


class StoreProductListIndexPageAPIView(StoreProductListAPIView):

    def get_queryset(self):
        return self.queryset.filter(
            inventory__gt=0
        ).annotate(
            min_price=Min('product__store_products__price')
        ).filter(
            price=F('min_price')
        ).annotate(
            order_count=Sum('order_items__quantity')
        ).distinct()
