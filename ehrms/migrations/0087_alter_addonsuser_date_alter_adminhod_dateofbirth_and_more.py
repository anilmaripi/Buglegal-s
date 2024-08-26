# Generated by Django 4.2.4 on 2024-01-05 08:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0086_adminnav_show1_adminnav_show2_adminnav_show3_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addonsuser',
            name='date',
            field=models.DateField(default=datetime.date(2024, 1, 5)),
        ),
        migrations.AlterField(
            model_name='adminhod',
            name='dateofbirth',
            field=models.DateField(default=datetime.date(2024, 1, 5)),
        ),
        migrations.AlterField(
            model_name='adminhod',
            name='dateofjoining',
            field=models.DateField(default=datetime.date(2024, 1, 5)),
        ),
        migrations.AlterField(
            model_name='companys',
            name='freetraile',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='employ_payslip',
            name='dateofbirth',
            field=models.DateField(default=datetime.date(2024, 1, 5)),
        ),
        migrations.AlterField(
            model_name='employeeloginlogout',
            name='login_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 5, 14, 8, 23, 618587)),
        ),
        migrations.AlterField(
            model_name='employs',
            name='dateofjoining',
            field=models.DateField(default=datetime.date(2024, 1, 5)),
        ),
        migrations.AlterField(
            model_name='hr',
            name='dateofbirth',
            field=models.DateField(default=datetime.date(2024, 1, 5)),
        ),
        migrations.AlterField(
            model_name='hr',
            name='dateofjoining',
            field=models.DateField(default=datetime.date(2024, 1, 5)),
        ),
        migrations.AlterField(
            model_name='projecttask',
            name='task_date',
            field=models.DateField(default=datetime.date(2024, 1, 5)),
        ),
        migrations.AlterField(
            model_name='tlassigntask',
            name='task_date',
            field=models.DateField(default=datetime.date(2024, 1, 5)),
        ),
    ]
