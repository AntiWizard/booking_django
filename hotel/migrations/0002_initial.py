# Generated by Django 4.1.4 on 2023-01-06 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservations', '0001_initial'),
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelroom',
            name='price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)ss_price', to='reservations.price'),
        ),
        migrations.AddField(
            model_name='hotelreservation',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservation', to='hotel.hotelroom'),
        ),
    ]
