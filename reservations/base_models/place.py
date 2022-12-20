from django.db import models


class AbstractPlace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.ForeignKey('reservations.PlaceType', related_name='%(app_label)s_%(class)s',
                             on_delete=models.PROTECT)

    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
