# Generated by Django 4.2.3 on 2023-12-12 07:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0028_monitoringdata_remove_monitoring_discription_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeindex2',
            name='image1',
        ),
        migrations.AlterField(
            model_name='projecttask',
            name='task_date',
            field=models.DateField(default=datetime.date(2023, 12, 12)),
        ),
        migrations.AlterField(
            model_name='tlassigntask',
            name='task_date',
            field=models.DateField(default=datetime.date(2023, 12, 12)),
        ),
    ]
