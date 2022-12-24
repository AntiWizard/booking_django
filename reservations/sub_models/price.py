from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=4)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.code = self.code.upper()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.code


class Price(models.Model):
    value = models.FloatField(default=0.0)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    ratio = models.FloatField(default=0.0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency')

    def __str__(self):
        return '{} ({})'.format(str(self.value), self.currency.code)


class CurrencyExchangeRate(models.Model):
    rate = models.FloatField()
    currency_from = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name="currency_from")
    currency_to = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name="currency_to")

    def __str__(self):
        return "{}/{}: {}".format(self.currency_from.code, self.currency_to.code, str(self.rate))

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('currency_from', 'currency_to'), name='unique_currency_from_currency_to'),
            models.CheckConstraint(
                check=~models.Q(currency_from=models.F('currency_to')),
                name='currency_from_and_currency_to_not_be_equal')
        ]
