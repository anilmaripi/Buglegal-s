# Generated by Django 4.2.4 on 2024-01-04 07:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0085_rename_login_login1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminnav',
            name='show1',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='adminnav',
            name='show2',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='adminnav',
            name='show3',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='employeeloginlogout',
            name='login_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 12, 42, 30, 841449)),
        ),
    ]
