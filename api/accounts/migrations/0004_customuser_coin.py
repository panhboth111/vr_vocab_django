# Generated by Django 3.1.4 on 2021-02-04 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='coin',
            field=models.IntegerField(default=0),
        ),
    ]
