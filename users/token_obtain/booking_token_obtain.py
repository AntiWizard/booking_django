from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_login_failed
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_variables
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class = AccessToken

    default_error_messages = {
        "invalid_account": _("invalid_account")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["otp"] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "otp": attrs["otp"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = booking_authenticate(**authenticate_kwargs)

        if not self.user:
            raise ValidationError("invalid_otp",)

        refresh = self.get_token(self.user)

        data = {}

        data["access"] = str(refresh)

        update_last_login(None, self.user)

        return data

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class BookingBackend(ModelBackend):
    def authenticate(self, request, username=None, otp=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or otp is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(otp)
        else:
            if otp == str(cache.get(username)) and self.user_can_authenticate(user):
                return user


@sensitive_variables("credentials")
def booking_authenticate(request=None, **credentials):
    backend = BookingBackend()
    user = backend.authenticate(request, **credentials)

    if user is None:
        user_login_failed.send(
            sender=__name__, request=request
        )

    return user
