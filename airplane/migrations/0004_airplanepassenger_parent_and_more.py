# Generated by Django 4.1.4 on 2023-01-02 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('airplane', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='airplanepassenger',
            name='parent',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='airplanepassenger',
            name='passenger_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]