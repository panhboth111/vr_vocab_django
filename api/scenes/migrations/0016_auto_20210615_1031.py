# Generated by Django 3.1.4 on 2021-06-15 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenes', '0015_auto_20210613_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='percentage',
            name='complete',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='percentage',
            name='percentage',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='percentage',
            name='total_vocab',
            field=models.IntegerField(default=0),
        ),
    ]
