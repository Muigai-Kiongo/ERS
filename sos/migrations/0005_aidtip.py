# Generated by Django 5.1.1 on 2025-03-05 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sos', '0004_alter_emergency_options_emergency_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='AidTip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emergency_type', models.CharField(max_length=50)),
                ('tip', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
