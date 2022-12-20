from django.db import models


class AbstractPlace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.ForeignKey('reservations.PlaceType', related_name='%(app_label)s_%(class)s',
                             on_delete=models.PROTECT)

    rate = models.OneToOneField('reservations.PlaceRate', on_delete=models.PROTECT)
    address = models.OneToOneField('reservations.PlaceAddress', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
