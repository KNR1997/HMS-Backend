# Generated by Django 4.2.17 on 2025-03-17 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_alter_booking_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ('CheckIn', 'CheckIn'), ('CheckOut', 'CheckOut')], default='Pending', max_length=20),
        ),
    ]
