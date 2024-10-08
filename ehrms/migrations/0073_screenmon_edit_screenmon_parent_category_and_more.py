# Generated by Django 4.2.4 on 2024-01-02 09:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0072_remove_freetraillimit_companyid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='screenmon',
            name='edit',
            field=models.BooleanField(default=1),
        ),
        migrations.AddField(
            model_name='screenmon',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subdrop', to='ehrms.screenmon'),
        ),
        migrations.AlterField(
            model_name='employeeloginlogout',
            name='login_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 2, 14, 58, 39, 573190)),
        ),
    ]
