# Generated by Django 5.0.1 on 2024-02-05 09:20

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0113_alter_employeeloginlogout_login_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeloginlogout',
            name='login_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 14, 50, 42, 298240)),
        ),
        migrations.AlterField(
            model_name='tlassigntask',
            name='companyid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ehrms.companys'),
        ),
    ]
