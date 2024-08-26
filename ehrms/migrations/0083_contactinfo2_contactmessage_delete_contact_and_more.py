# Generated by Django 4.2.4 on 2024-01-04 05:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0082_about_alter_employeeloginlogout_login_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfo2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('phone_hours', models.CharField(max_length=50)),
                ('email_addresses', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='Contact1',
        ),
        migrations.AlterField(
            model_name='employeeloginlogout',
            name='login_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 11, 8, 6, 64864)),
        ),
    ]
