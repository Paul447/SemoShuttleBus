# Generated by Django 5.1.2 on 2024-11-29 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluegreen', '0007_blueshuttle_occupancy_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blueshuttle',
            name='time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]