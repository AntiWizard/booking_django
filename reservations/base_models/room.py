from django.db import models


class AbstractRoom(models.Model):
    number = models.PositiveSmallIntegerField()
    capacity = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    price_per_night = models.OneToOneField("reservations.Price", null=True, on_delete=models.SET_NULL)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractSeat(models.Model):
    number = models.PositiveSmallIntegerField()
    capacity = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    price_per_night = models.OneToOneField("reservations.Price", null=True, on_delete=models.SET_NULL)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
