# Generated by Django 5.1.2 on 2024-10-24 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluegreen', '0004_alter_blueshuttle_number_of_passangers_in_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastStopBlueOccupancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blue_occupancy', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LastStopGreenOccupancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('green_occupancy', models.IntegerField(default=0)),
            ],
        ),
    ]