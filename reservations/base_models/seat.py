from django.db import models


class ReservedStatus(models.TextChoices):
    FREE = "FREE"
    INVALID = "INVALID"
    RESERVED = "RESERVED"


class AbstractSeat(models.Model):
    number = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=10, choices=ReservedStatus.choices, default=ReservedStatus.FREE)
    price = models.OneToOneField("reservations.Price", null=True, on_delete=models.SET_NULL)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
