# Generated by Django 4.2.4 on 2023-12-04 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0015_checkin_is_employee_checkout_is_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_details',
            name='companyid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ehrms.companys'),
        ),
        migrations.AddField(
            model_name='companys',
            name='profilepic',
            field=models.ImageField(default='', upload_to='media/'),
        ),
    ]
