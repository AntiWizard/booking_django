# Generated by Django 4.1.4 on 2022-12-20 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('airplane', '0001_initial'),
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='airplanereservation',
            name='total_cost',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='reservations.price'),
        ),
    ]
