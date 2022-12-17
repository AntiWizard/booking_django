# Generated by Django 4.1.4 on 2022-12-17 13:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utlis.validation_zip_code


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_address_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('IR', 'Iran'), ('UK', 'United Kingdom')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_coordination', models.FloatField(blank=True, null=True)),
                ('y_coordination', models.FloatField(blank=True, null=True)),
                ('is_valid', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must not consist of space and requires country code. eg : 989210000000', regex='^[1-9][0-9]{8,14}$')])),
                ('address', models.TextField(blank=True, null=True)),
                ('zip_code', models.BigIntegerField(blank=True, null=True, validators=[utlis.validation_zip_code.validation_zip_code])),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='users.city')),
                ('location', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='users.location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'auth'},
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='auth/avatars/'),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='users.country'),
        ),
    ]