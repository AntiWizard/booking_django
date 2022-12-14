from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User, Address
from users.permissions import IsOwner, IsAnonymous
from users.serializers import UserSerializer, AddressSerializer, LoginSerializer, OTPSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
    })


class ListUserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = LimitOffsetPagination
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]


class LoginUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [IsAnonymous]

    # throttle_scope = 'create_user'

    def post(self, request, *args, **kwargs):
        # requests.get("http://127.0.0.1:8000/user/otp/", data=request.data)
        phone = request.data['phone']
        otp = cache.get(phone)
        if otp == request.data["otp"]:
            user = User.objects.filter(phone=phone)
            if not user.exists():
                return super().post(request, *args, **kwargs)
        else:
            raise ValidationError("{} invalid otp".format(request.data["otp"]))


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
            return Address.objects.get(phone=user.get().phone)
        return super(DetailAddressAPIView, self).get_object()

    def perform_update(self, serializer):
        if serializer.validated_data.get('city'):
            serializer.validated_data['city'] = serializer.validated_data['city'].title()
        serializer.save()


class GenerateOTP(generics.ListAPIView):
    serializer_class = OTPSerializer
    throttle_classes = [AnonRateThrottle]

    def list(self, request, *args, **kwargs):
        code = {"otp": "11111"}
        if request.data.get('phone'):  # check phone correct logic
            cache.set(request.data['phone'], code["otp"], 60 * 2)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(code)
        return Response(serializer.data)
