# Generated by Django 2.1.5 on 2020-01-13 20:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 1, 13, 22, 21, 32, 150765)),
        ),
    ]
