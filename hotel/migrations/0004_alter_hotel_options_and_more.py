# Generated by Django 4.1.4 on 2022-12-30 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotel',
            options={'ordering': ['-star']},
        ),
        migrations.RenameField(
            model_name='hotelroom',
            old_name='price_per_night',
            new_name='price',
        ),
    ]
