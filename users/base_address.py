from django.core.validators import RegexValidator
from django.db import models


class Country(models.Model):
    class CountryChoice(models.TextChoices):
        IRAN = "IRAN"
        UNITED_STATE = "UNITED STATE"

    name = models.CharField(max_length=100, choices=CountryChoice.choices, null=True, blank=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name='cities', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Location(models.Model):
    x_coordination = models.FloatField(null=True, blank=True)
    y_coordination = models.FloatField(null=True, blank=True)
    is_valid = models.BooleanField(default=True)


class AbstractAddress(models.Model):
    phone_regex = RegexValidator(regex=r'^[1-9][0-9]{8,14}$',
                                 message="Phone number must not consist of space and requires country code. eg : "
                                         "989210000000")
    phone = models.CharField(validators=[phone_regex], max_length=16, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='%(class)ss', null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    location = models.OneToOneField(Location, on_delete=models.PROTECT, null=True)

    def __str__(self):
        if self.location:
            return '{}:{} - ({},{})'.format(self.city.country.name, self.city.name, self.location.x_coordination,
                                            self.location.y_coordination)
        else:
            return "{}:{}".format(self.city.country.name, self.city.name)

    class Meta:
        abstract = True
