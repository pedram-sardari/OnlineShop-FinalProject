from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import StoreProductVendorsSerializer
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

class StoreProductListAPIView(ListAPIView):
    pass
