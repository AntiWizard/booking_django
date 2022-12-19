import json

import requests
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import AnonRateThrottle

from users.auth.serializers import OTPSerializer, LoginSerializer
from users.models import User
from users.permissions import IsAnonymous
from users.tasks import send_sms_to_user
from utlis.auth.otp_generator import otp_generator


class GenerateOTP(generics.ListAPIView):  # TODO logic -> serializer
    serializer_class = OTPSerializer
    throttle_classes = [AnonRateThrottle]

    def list(self, request, *args, **kwargs):
        if request.data.get('phone'):  # TODO check phone correct logic
            otp = otp_generator(10000, 99999)
            code = {"otp": otp}
            cache.set(request.data['phone'], code["otp"], 60 * 2)

        else:
            data = {"error": "phone field required"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(code)

        send_sms_to_user.delay(request.data['phone'], str(otp))

        return Response(serializer.data)


class LoginUserAPIView(generics.CreateAPIView):  # TODO logic -> serializer
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [IsAnonymous]

    # throttle_scope = 'create_user'

    def post(self, request, *args, **kwargs):
        if request.data.get('phone') and request.data.get('otp'):  # TODO check phone correct logic
            phone = request.data['phone']

            user_otp = cache.get(phone)

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
                raise AuthenticationFailed("{} invalid otp".format(request.data["otp"]))

        else:
            data = {"error": "phone and otp fields required"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
