# Generated by Django 3.1.4 on 2021-06-13 12:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210607_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='last_request',
            field=models.DateTimeField(default=datetime.date(2021, 6, 12), null=True),
        ),
    ]