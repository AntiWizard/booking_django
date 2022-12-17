from django.core.exceptions import ValidationError


def validation_zip_code(value):
    if not len(str(value)) in [4, 5, 10]:
        raise ValidationError(
            "%(value)s is invalid"
            , params={"value": value}
        )
