# Generated by Django 4.2.4 on 2024-01-09 09:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0089_payslip_request_companyid_alter_addonsuser_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetracking3',
            name='icons',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='addonsuser',
            name='date',
            field=models.DateField(default=datetime.date(2024, 1, 9)),
        ),
        migrations.AlterField(
            model_name='adminhod',
            name='dateofbirth',
            field=models.DateField(default=datetime.date(2024, 1, 9)),
        ),
        migrations.AlterField(
            model_name='adminhod',
            name='dateofjoining',
            field=models.DateField(default=datetime.date(2024, 1, 9)),
        ),
        migrations.AlterField(
            model_name='employ_payslip',
            name='dateofbirth',
            field=models.DateField(default=datetime.date(2024, 1, 9)),
        ),
        migrations.AlterField(
            model_name='employeeloginlogout',
            name='login_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 9, 14, 47, 46, 653379)),
        ),
        migrations.AlterField(
            model_name='employs',
            name='dateofjoining',
            field=models.DateField(default=datetime.date(2024, 1, 9)),
        ),
        migrations.AlterField(
            model_name='hr',
            name='dateofbirth',
            field=models.DateField(default=datetime.date(2024, 1, 9)),
        ),
        migrations.AlterField(
            model_name='hr',
            name='dateofjoining',
            field=models.DateField(default=datetime.date(2024, 1, 9)),
        ),
        migrations.AlterField(
            model_name='projecttask',
            name='task_date',
            field=models.DateField(default=datetime.date(2024, 1, 9)),
        ),
        migrations.AlterField(
            model_name='tlassigntask',
            name='task_date',
            field=models.DateField(default=datetime.date(2024, 1, 9)),
        ),
    ]
