from django.core.validators import RegexValidator
from django.db import models

from utlis.validation_zip_code import validation_zip_code


class AbstractAddress(models.Model):
    phone_regex = RegexValidator(regex=r'^[1-9][0-9]{8,14}$',
                                 message="Phone number must not consist of space and requires country code. eg : "
                                         "989210000000")
    phone = models.CharField(validators=[phone_regex], max_length=16, unique=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    zip_code = models.BigIntegerField(validators=[validation_zip_code], blank=True, null=True)
    location = models.OneToOneField("reservations.Location", on_delete=models.PROTECT, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.country = self.country.upper() if self.country else None
        self.city = self.city.capitalize() if self.country else None
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return "{} : {}".format(self.country, self.city)

    class Meta:
        abstract = True
