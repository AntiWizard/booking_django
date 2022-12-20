from django.db import models

from reservations.base_models.address import AbstractAddress
from utlis.validation_zip_code import validation_zip_code


class PlaceAddress(AbstractAddress):
    zip_code = models.BigIntegerField(validators=[validation_zip_code], blank=True, null=True)

    def __str__(self):
        return "{}:{}".format(self.country, self.city)


class TransportAddress(AbstractAddress):

    def __str__(self):
        return "{}:{}".format(self.country, self.city)
