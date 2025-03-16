# Generated by Django 5.1.1 on 2025-03-16 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0006_remove_emergencycontacts_emergency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergency',
            name='location',
            field=models.CharField(choices=[('location_1', 'Thika Town'), ('location_2', 'Bidco'), ('location_3', 'Runda'), ('location_4', 'Starehe'), ('location_5', 'MKU'), ('location_6', 'Thika Level 5'), ('location_7', 'Kiandutu'), ('location_8', 'Biafra')], default='location_1', help_text='Select the location of the emergency', max_length=20),
        ),
    ]
