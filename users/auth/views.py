from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from users.auth.serializers import OTPSerializer, LoginSerializer
from users.models import User
from users.permissions import IsAnonymous
from users.tasks import send_sms_to_user
from utlis.auth.otp_generator import otp_generator


class GenerateOTP(generics.CreateAPIView):
    serializer_class = OTPSerializer
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        if request.data.get('phone'):
            otp = otp_generator(10000, 99999)
            cache.set(request.data['phone'], otp, 60 * 2)

        else:
            data = {"error": "phone field required"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        send_sms_to_user.delay(request.data['phone'], otp)

        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [IsAnonymous]

    def post(self, request, *args, **kwargs):
        if request.data.get('phone') and request.data.get('otp'):
            phone = request.data['phone']
            otp = request.data["otp"]

            user_otp = cache.get(phone)

            if user_otp == otp:
                try:
                    user = User.objects.get(phone=phone)
                except User.DoesNotExist:
                    user = User.objects.create_user(phone=phone)

                refresh = RefreshToken.for_user(user)
                context = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(context)
            else:
                raise AuthenticationFailed("{} invalid otp".format(request.data["otp"]))

        else:
            data = {"error": "phone and otp fields required"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
