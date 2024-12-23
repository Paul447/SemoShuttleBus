# Generated by Django 5.1.2 on 2024-10-22 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluegreen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='greenShuttleStopIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('green_index_value', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='greenshuttle',
            name='location_name',
        ),
        migrations.AddField(
            model_name='greenshuttle',
            name='stop_name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='greenshuttle',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='greenshuttle',
            name='time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
