# Generated by Django 4.2.4 on 2023-12-05 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0020_alter_admin_drop_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin_drop',
            name='parentshow',
            field=models.BooleanField(default=0),
        ),
    ]
