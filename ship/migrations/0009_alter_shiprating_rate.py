# Generated by Django 4.1.4 on 2022-12-29 16:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ship', '0008_remove_shipreservation_total_cost_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiprating',
            name='rate',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
