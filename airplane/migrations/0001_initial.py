# Generated by Django 4.1.4 on 2023-01-06 09:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utlis.validation_transport_date
import utlis.validation_zip_code
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airplane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transport_number', models.IntegerField(default=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('max_reservation', models.PositiveSmallIntegerField()),
                ('number_reserved', models.PositiveSmallIntegerField(default=0)),
                ('transfer_date', models.DateTimeField(validators=[utlis.validation_transport_date.validation_transport_date])),
                ('duration', models.TimeField()),
                ('transport_status', models.CharField(choices=[('SPACE', 'Space'), ('FULL', 'Full'), ('TRANSFER', 'Transfer'), ('ARRIVED', 'Arrived'), ('CANCELLED', 'Cancelled')], default='SPACE', max_length=15)),
                ('is_valid', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('pilot', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['-transport_number'],
            },
        ),
        migrations.CreateModel(
            name='AirplaneCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AirplaneCompanyComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_body', models.TextField()),
                ('status', models.CharField(choices=[('CREATED', 'Created'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('DELETED', 'Deleted')], default='CREATED', max_length=15)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AirplaneCompanyRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('is_valid', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AirplanePassenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_code', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('reserved_key', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must not consist of space and requires country code. eg : 989210000000', regex='^[1-9][0-9]{8,14}$')])),
                ('birth_day', models.DateField()),
                ('national_id', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('passenger_type', models.CharField(choices=[('ADULT', 'Adult'), ('CHILDREN', 'Children')], default='ADULT', max_length=20)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('transfer_status', models.CharField(choices=[('INITIAL', 'Initial'), ('RESERVED', 'Reserved'), ('TRANSFER', 'Transfer'), ('ARRIVED', 'Arrived'), ('CANCELLED', 'Cancelled')], default='INITIAL', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='AirplaneReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserved_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('reserved_status', models.CharField(choices=[('INITIAL', 'Initial'), ('RESERVED', 'Reserved'), ('CANCELLED', 'Cancelled'), ('FINISHED', 'Finished'), ('PROBLEM', 'Problem')], default='INITIAL', max_length=15)),
                ('is_valid', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('passenger_count', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AirplaneSeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField()),
                ('status', models.CharField(choices=[('INITIAL', 'Initial'), ('FREE', 'Free'), ('RESERVED', 'Reserved'), ('PROBLEM', 'Problem')], default='FREE', max_length=10)),
                ('is_valid', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AirportAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must not consist of space and requires country code. eg : 989210000000', regex='^[1-9][0-9]{8,14}$')])),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('zip_code', models.BigIntegerField(blank=True, null=True, validators=[utlis.validation_zip_code.validation_zip_code])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AirportTerminal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(default=1)),
                ('is_valid', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='airport', to='airplane.airport')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
