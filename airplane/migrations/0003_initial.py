# Generated by Django 4.1.4 on 2022-12-29 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservations', '0001_initial'),
        ('airplane', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='airplanereservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='airplanerating',
            name='airplane',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate', to='airplane.airplane'),
        ),
        migrations.AddField(
            model_name='airplanerating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='airplaneaddress',
            name='location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='reservations.location'),
        ),
        migrations.AddField(
            model_name='airplane',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destination', to='airplane.airplaneaddress'),
        ),
        migrations.AddField(
            model_name='airplane',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='source', to='airplane.airplaneaddress'),
        ),
        migrations.AddConstraint(
            model_name='airplaneseat',
            constraint=models.UniqueConstraint(fields=('airplane', 'number'), name='unique_airplane_seat'),
        ),
        migrations.AddConstraint(
            model_name='airplanereservation',
            constraint=models.UniqueConstraint(fields=('user', 'seat'), name='unique_user_airplane_seat'),
        ),
        migrations.AddConstraint(
            model_name='airplanerating',
            constraint=models.UniqueConstraint(fields=('airplane', 'user', 'rate'), name='unique_airplane_user_rate'),
        ),
        migrations.AddConstraint(
            model_name='airplane',
            constraint=models.UniqueConstraint(condition=models.Q(('transport_status__in', ['SPACE', 'TRANSFER'])), fields=('pilot', 'transport_status'), name='unique_pilot_transport_status'),
        ),
    ]