# Generated by Django 5.0.6 on 2024-07-03 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='seat',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
