# Generated by Django 4.2.13 on 2024-05-26 20:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_remove_usage_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='usage',
            name='month',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
