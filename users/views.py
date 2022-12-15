import json

import requests as requests
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
from users.tasks import send_sms_to_user
from utlis.users.otp_generator import otp_generator


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'swagger': reverse('swagger-ui', request=request, format=format),
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
        if request.data.get('phone'):  # TODO check phone correct logic
            otp = otp_generator(10000, 99999)
            code = {"otp": otp}
            cache.set(request.data['phone'], code["otp"], 60 * 12)

        else:
            data = {"error": "phone field required"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(code)

        send_sms_to_user.delay(request.data['phone'], str(otp))

        return Response(serializer.data)


class LoginUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [IsAnonymous]

    # throttle_scope = 'create_user'

    def post(self, request, *args, **kwargs):
        if request.data.get('phone') and request.data.get('otp'):  # TODO check phone correct logic
            phone = request.data['phone']

            user_otp = cache.get(phone)
            cache.delete(request.data['phone'])

            if str(user_otp) == request.data["otp"]:
                user = User.objects.filter(phone=phone)

                if not user.exists():
                    super().post(request, *args, **kwargs)

                response_login = requests.post(
                    request.build_absolute_uri(reverse('token_obtain')),
                    data={"phone": request.data['phone'], "otp": request.data["otp"]})

                token = json.loads(response_login.content)
                return Response(token, response_login.status_code)

            else:
                raise ValidationError("{} invalid otp".format(request.data["otp"]))

        else:
            data = {"error": "phone and otp fields required"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
