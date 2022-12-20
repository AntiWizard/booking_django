from django.db import models


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
