# Generated by Django 3.1.4 on 2021-03-17 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20210317_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='last_request',
            field=models.DateTimeField(default='0000-00-00 00:00:[:00[.000000]][0Z]', null=True),
        ),
    ]
