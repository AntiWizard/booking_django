from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import UserRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User, UserAddress
from users.permissions import IsOwner
from users.serializers import UserSerializer, AddressSerializer


@api_view(['GET'])
def api_schema(request, _format=None):
    return Response({
        'swagger': reverse('swagger-ui', request=request, format=_format),
        'api': reverse('api-view_list', request=request, format=_format),
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

        user = get_object_or_404(User, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, user)
        return get_object_or_404(UserAddress, phone=user.phone)
