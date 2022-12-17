from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User, UserAddress
from users.permissions import IsOwner
from users.serializers import UserSerializer, AddressSerializer


@api_view(['GET'])
def api_root(request, _format=None):
    return Response({
        'swagger': reverse('swagger-ui', request=request, format=_format),
    })


class ListUserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = LimitOffsetPagination
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]


class DetailUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        if self.request.data.get('nationality'):
            self.request.data._mutable = True
            self.request.data['nationality'] = self.request.data['nationality'].upper()
            self.request.data._mutable = False

        if self.request.data.get('gender'):
            self.request.data._mutable = True
            self.request.data['gender'] = self.request.data['gender'].upper()
            self.request.data._mutable = False

        return super(DetailUserAPIView, self).get_queryset()

    def perform_destroy(self, instance):
        instance.is_valid = False
        instance.save()


class DetailAddressAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsOwner]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def get_object(self):
        if self.request.data.get('nationality'):
            self.request.data._mutable = True
            self.request.data['nationality'] = self.request.data['nationality'].upper()
            self.request.data._mutable = False

        user = User.objects.filter(pk=self.kwargs['pk'])
        if user.exists():
            return UserAddress.objects.get(phone=user.get().phone)

        return super(DetailAddressAPIView, self).get_object()

    def perform_update(self, serializer):
        if serializer.validated_data.get('city'):
            serializer.validated_data['city'] = serializer.validated_data['city'].title()
        serializer.save()
