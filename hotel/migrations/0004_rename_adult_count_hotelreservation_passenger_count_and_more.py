# Generated by Django 4.1.4 on 2023-01-02 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotelreservation',
            old_name='adult_count',
            new_name='passenger_count',
        ),
        migrations.RemoveField(
            model_name='hotelreservation',
            name='children_count',
        ),
    ]