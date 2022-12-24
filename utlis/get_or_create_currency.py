from reservations.sub_models.price import Currency


def get_or_create_currency(currency):
    return Currency.objects.get_or_create(name=currency.get('name', None),
                                          defaults={"code": currency["code"]})
