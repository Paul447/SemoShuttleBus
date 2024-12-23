# Generated by Django 5.1.2 on 2024-10-22 16:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationAdder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=200)),
                ('is_blue', models.BooleanField(default=False)),
                ('is_green', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Shuttle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shuttle_name', models.CharField(max_length=200)),
                ('shuttle_capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ShuttleStopIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blue_index_value', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GreenShuttle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mu_name', models.CharField(default='Green', max_length=200)),
                ('number_of_passangers_in', models.IntegerField()),
                ('number_of_passangers_out', models.IntegerField()),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('shuttle_driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('location_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bluegreen.locationadder')),
                ('shuttle_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bluegreen.shuttle')),
            ],
        ),
        migrations.CreateModel(
            name='BlueShuttle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mu_name', models.CharField(default='Blue', max_length=200)),
                ('stop_name', models.CharField(max_length=200)),
                ('number_of_passangers_in', models.IntegerField()),
                ('number_of_passangers_out', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('time', models.TimeField(auto_now_add=True, null=True)),
                ('shuttle_driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('shuttle_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bluegreen.shuttle')),
            ],
        ),
    ]
