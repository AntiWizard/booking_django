from reservations.base_models.address import AbstractAddress
from reservations.base_models.comment import AbstractComment
from reservations.base_models.passenger import AbstractPassenger, TransferStatus
from reservations.base_models.rate import AbstractRate
from reservations.base_models.reservation import AbstractReservation
from reservations.base_models.seat import AbstractSeat
from reservations.base_models.transport import *

# ---------------------------------------------Airport------------------------------------------------------------------
from reservations.sub_models.price import Price


class Airport(AbstractTransport):
    address = models.ForeignKey("AirportAddress", on_delete=models.PROTECT, related_name='airport')


class AirportTerminal(AbstractTerminal):
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="airport")

    def __str__(self):
        return "{} : {}".format(self.airport.title, self.number)


class AirplaneCompany(AbstractTransportCompany):
    airport_terminal = models.ForeignKey(AirportTerminal, on_delete=models.CASCADE, related_name="airport_terminal")

    @property
    def average_rating(self):
        rate = AirplaneCompanyRating.objects.filter(company=self).all().aggregate(avg=models.Avg('rate'))
        return rate.get('avg') or 5

    def __str__(self):
        return "{} : {}".format(self.airport_terminal.airport.title, self.name)


# ---------------------------------------------Airplane-----------------------------------------------------------------

class Airplane(AbstractTransfer):
    company = models.ForeignKey(AirplaneCompany, on_delete=models.CASCADE, related_name="airplane")
    pilot = models.CharField(max_length=50)
    source = models.ForeignKey(Airport, on_delete=models.PROTECT,
                               related_name='source')
    destination = models.ForeignKey(Airport, on_delete=models.PROTECT,
                                    related_name='destination')

    @property
    def average_rating(self):
        rate = AirplaneCompanyRating.objects.filter(company__airplane=self).all().aggregate(avg=models.Avg('rate'))
        return rate.get('avg') or 5

    @property
    def price_per_seat(self):
        price = AirplaneSeat.objects.filter(airplane=self).first()
        return price.price or -1

    def __str__(self):
        return "{} : {}".format(self.transport_number, self.pilot)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.pilot = self.pilot.title()

        last_number = Airplane.objects.all().order_by('-transport_number').first()
        if last_number:
            self.transport_number = last_number.transport_number + 1

        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ['-transport_number']
        constraints = [models.UniqueConstraint(
            condition=models.Q(
                transport_status__in=[TransportStatus.SPACE, TransportStatus.TRANSFER]),
            fields=('pilot', 'transport_status'), name='unique_pilot_transport_status')]


# ---------------------------------------------AirplaneSeat-------------------------------------------------------------

class AirplaneSeat(AbstractSeat):
    airplane = models.ForeignKey(Airplane, related_name='seat', on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.airplane.id, self.number)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('airplane', 'number'), name='unique_airplane_seat')]


# ---------------------------------------------Passengers-------------------------------------------------------------

class AirplanePassenger(AbstractPassenger):
    seat = models.ForeignKey(AirplaneSeat, related_name='seat', on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {} - {} -> {}".format(self.seat.airplane.company.airport_terminal.airport.title
                                          , self.seat.airplane.transport_number, self.seat.number, self.phone)

    class Meta:
        constraints = [models.UniqueConstraint(
            condition=models.Q(
                transfer_status__in=[TransferStatus.INITIAL, TransferStatus.RESERVED, TransferStatus.TRANSFER])
            , fields=('seat', 'phone'), name='unique_seat_user')]


# ---------------------------------------------AirplaneReservation------------------------------------------------------

class AirplaneReservation(AbstractReservation):
    airplane = models.ForeignKey(Airplane, on_delete=models.PROTECT, related_name="airplane_reservation")
    passenger_count = models.PositiveSmallIntegerField()

    def __str__(self):
        return "{} - {} - {}".format(self.user.phone, self.airplane.company.airport_terminal.airport.title,
                                     self.airplane.transport_number)


# ---------------------------------------------AirplaneRate-------------------------------------------------------------

class AirplaneCompanyRating(AbstractRate):
    company = models.ForeignKey(AirplaneCompany, on_delete=models.CASCADE, related_name='rate')

    def __str__(self):
        return "{} got {} from {}".format(self.company.name, self.rate, self.user.phone)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('company', 'user', 'rate'), name='unique_company_user_rate')]


# ---------------------------------------------AirplaneAddress----------------------------------------------------------

class AirportAddress(AbstractAddress):
    pass


# ---------------------------------------------AirplaneCompanyComment----------------------------------------------------


class AirplaneCompanyComment(AbstractComment):
    company = models.ForeignKey(AirplaneCompany, on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        return "{}: {}".format(self.company.name, self.comment_body[:10])
