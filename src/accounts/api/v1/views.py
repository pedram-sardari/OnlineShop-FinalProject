from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import UserAddressSerializer


class UserAddressCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]  # todo: handle in action method to prevent browser pop up for user and pass
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return self.request.user.addresses.all()

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class AuthenticationStatusAPIView(APIView):
    def get(self, request):
        if self.request.user.is_authenticated:
            return Response({'is_authenticated': True}, status=status.HTTP_200_OK)
        return Response({'is_authenticated': False}, status=status.HTTP_200_OK)
