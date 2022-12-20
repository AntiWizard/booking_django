# Generated by Django 4.1.2 on 2022-12-20 21:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utlis.validation_zip_code


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='')),
                ('star', models.PositiveSmallIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('max_reservation', models.PositiveSmallIntegerField(default=100)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s', to='reservations.placetype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField()),
                ('capacity', models.PositiveSmallIntegerField()),
                ('description', models.TextField(blank=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_room', to='hotel.hotel')),
                ('price_per_night', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservations.price')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult_count', models.PositiveSmallIntegerField(default=0)),
                ('children_count', models.PositiveSmallIntegerField(default=0)),
                ('is_valid', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('check_in_date', models.DateTimeField()),
                ('check_out_date', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='hotel_reservation', to='hotel.hotelroom')),
                ('total_cost', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='reservations.price')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate', to='hotel.hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must not consist of space and requires country code. eg : 989210000000', regex='^[1-9][0-9]{8,14}$')])),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('zip_code', models.BigIntegerField(blank=True, null=True, validators=[utlis.validation_zip_code.validation_zip_code])),
                ('location', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='reservations.location')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]