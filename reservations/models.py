from django.conf import settings
from django.db import models


class AbstractReservationPlace(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s')
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    adult_count = models.PositiveSmallIntegerField(default=0)
    children_count = models.PositiveSmallIntegerField(default=0)
    total_cost = models.OneToOneField("reservations.Price", on_delete=models.PROTECT)

    class Meta:
        abstract = True


class AbstractReservationFlight(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s')
    check_source_date = models.DateTimeField()
    check_destination_date = models.DateTimeField(null=True)
    adult_count = models.PositiveSmallIntegerField(default=0)
    children_count = models.PositiveSmallIntegerField(default=0)
    total_cost = models.OneToOneField("reservations.Price", on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Currency(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=4)

    def __str__(self):
        return self.code


class Price(models.Model):
    value = models.FloatField(default=0.0)
    currency = models.OneToOneField(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(str(self.value), self.currency.code)


class CurrencyExchangeRate(models.Model):
    rate = models.FloatField()
    currency_from = models.OneToOneField('Currency', on_delete=models.CASCADE, related_name="currency_from")
    currency_to = models.OneToOneField('Currency', on_delete=models.CASCADE, related_name="currency_to")

    def __str__(self):
        return "{}/{}: {}".format(self.currency_from.code, self.currency_to.code, str(self.rate))
