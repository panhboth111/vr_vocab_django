# Generated by Django 3.1.4 on 2021-06-13 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenes', '0014_auto_20210613_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchased_scene',
            name='scene_id',
            field=models.IntegerField(default=0),
        ),
    ]
