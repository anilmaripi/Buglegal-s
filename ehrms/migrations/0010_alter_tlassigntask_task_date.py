# Generated by Django 4.2.4 on 2023-11-30 12:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0009_remove_employs_dateofbirth_remove_employs_o_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tlassigntask',
            name='task_date',
            field=models.DateField(default=datetime.date(2023, 11, 30)),
        ),
    ]
