# Generated by Django 4.2.4 on 2023-12-28 12:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0067_alter_adminhod_dateofbirth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminhod',
            name='dateofjoining',
            field=models.DateField(default=datetime.date(2023, 12, 28)),
        ),
        migrations.AlterField(
            model_name='employeeloginlogout',
            name='login_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 28, 17, 56, 33, 752770)),
        ),
        migrations.AlterField(
            model_name='employs',
            name='dateofjoining',
            field=models.DateField(default=datetime.date(2023, 12, 28)),
        ),
        migrations.AlterField(
            model_name='hr',
            name='dateofjoining',
            field=models.DateField(default=datetime.date(2023, 12, 28)),
        ),
        migrations.AlterField(
            model_name='working_shifts',
            name='ending_time',
            field=models.TimeField(default='23:00'),
        ),
    ]
