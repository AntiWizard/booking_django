# Generated by Django 4.1.4 on 2023-01-02 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservations', '0001_initial'),
        ('hotel', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelreservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hotelrating',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate', to='hotel.hotel'),
        ),
        migrations.AddField(
            model_name='hotelrating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hotelimage',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_image', to='hotel.hotelgallery'),
        ),
        migrations.AddField(
            model_name='hotelgallery',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='hotel_gallery', to='hotel.hotel'),
        ),
        migrations.AddField(
            model_name='hotelcomment',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_comment', to='hotel.hotel'),
        ),
        migrations.AddField(
            model_name='hotelcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent_%(class)ss', to='hotel.hotelcomment'),
        ),
        migrations.AddField(
            model_name='hotelcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hotelcomment',
            name='validated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='validated_%(class)ss', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hoteladdress',
            name='location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='reservations.location'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='hotel_address', to='hotel.hoteladdress'),
        ),
        migrations.AddConstraint(
            model_name='hotelroom',
            constraint=models.UniqueConstraint(fields=('hotel', 'number'), name='unique_hotel_number_seat'),
        ),
        migrations.AddConstraint(
            model_name='hotelreservation',
            constraint=models.UniqueConstraint(condition=models.Q(('reserved_status__in', ['INITIAL', 'RESERVED'])), fields=('user', 'room'), name='unique_user_hotel_room'),
        ),
        migrations.AddConstraint(
            model_name='hotelrating',
            constraint=models.UniqueConstraint(fields=('hotel', 'user', 'rate'), name='unique_hotel_user_rate'),
        ),
        migrations.AddConstraint(
            model_name='hotelimage',
            constraint=models.UniqueConstraint(condition=models.Q(('is_main', True)), fields=('gallery', 'is_main'), name='just_one_main_image'),
        ),
        migrations.AddConstraint(
            model_name='hotel',
            constraint=models.UniqueConstraint(fields=('name', 'residence_status'), name='unique_hotel_name_residence_status'),
        ),
    ]
