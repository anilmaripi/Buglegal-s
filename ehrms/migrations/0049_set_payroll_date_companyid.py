# Generated by Django 4.2.5 on 2023-12-19 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0048_employlev_companyid'),
    ]

    operations = [
        migrations.AddField(
            model_name='set_payroll_date',
            name='companyid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='ehrms.companys'),
        ),
    ]
