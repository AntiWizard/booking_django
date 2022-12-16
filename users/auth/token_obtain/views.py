from rest_framework_simplejwt.views import TokenObtainPairView

from users.auth.token_obtain.serializers import TokenAPISerializer


class TokenAPIView(TokenObtainPairView):
    serializer_class = TokenAPISerializer
