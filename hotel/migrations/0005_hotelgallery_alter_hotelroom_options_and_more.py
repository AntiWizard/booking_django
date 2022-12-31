# Generated by Django 4.1.4 on 2022-12-30 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_alter_hotel_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('is_valid', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='hotelroom',
            options={'ordering': ['price']},
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='avatar',
        ),
        migrations.CreateModel(
            name='HotelImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='get_place_images_upload_location')),
                ('is_valid', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_image', to='hotel.hotelgallery')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='hotelgallery',
            name='hotel',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='hotel_gallery', to='hotel.hotel'),
        ),
    ]
