# Generated by Django 4.2.17 on 2025-03-08 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='room',
        ),
    ]
