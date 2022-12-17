from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.base_address import Country, City
from users.models import User, UserAddress
from users.permissions import IsOwner
from users.serializers import UserSerializer, AddressSerializer


@api_view(['GET'])
def api_root(request, _format=None):
    return Response({
        'swagger': reverse('swagger-ui', request=request, format=_format),
    })


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
        city = self.request.data.get('city')
        if city:
            country = city.get('country')
            if country and Country.objects.filter(id=country.get('id')).exists():
                City.objects.get_or_create(country_id=country['id'], name=city.get('name', self.get_object().city.name))
        serializer.save()
