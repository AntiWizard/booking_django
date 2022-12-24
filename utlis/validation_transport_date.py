from django.core.exceptions import ValidationError
from django.utils import timezone


def validation_transport_date(value):
    if value < timezone.now():
        raise ValidationError(
            "%(value)s is invalid"
            , params={"value": value}
        )
