from django.db import models

from reservations.base_rate import AbstractRate
from users.base_address import AbstractAddress
from utlis.validation_zip_code import validation_zip_code


class AbstractPlace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.ForeignKey('place.PlaceType', related_name='%(app_label)s_%(class)s', on_delete=models.PROTECT)
    rate = models.OneToOneField('place.PlaceRate', on_delete=models.PROTECT)
    address = models.OneToOneField('place.PlaceAddress', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class PlaceType(models.Model):
    class PlaceTypeChoice(models.TextChoices):
        BUSINESS = "BUSINESS"
        HOLIDAY = "HOLIDAY"

    title = models.CharField(max_length=40, choices=PlaceTypeChoice.choices)

    def __str__(self):
        return self.title


class PlaceAddress(AbstractAddress):
    zip_code = models.BigIntegerField(validators=[validation_zip_code], blank=True, null=True)

    def __str__(self):
        if self.location:
            return '{}:{} - ({},{})'.format(self.city.country.name, self.city.name, self.location.x_coordination,
                                            self.location.y_coordination)
        else:
            return "{}:{}".format(self.city.country.name, self.city.name)


class PlaceRate(AbstractRate):
    pass
