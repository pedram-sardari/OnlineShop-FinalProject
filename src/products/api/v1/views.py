from django.db.models import Sum
from rest_framework import filters
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from vendors.models import Store
from website.paginations import MyPagination
from .serializer import StoreProductVendorsSerializer, StoreSerializer
from products.models import StoreProduct


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
    ordering_fields = ['id', 'created_at', 'orders_count']
    ordering = ['id']
