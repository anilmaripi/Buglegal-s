# Generated by Django 4.2.4 on 2023-11-29 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehrms', '0002_alter_employs_dateofbirth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employs',
            name='dateofbirth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employs',
            name='dateofjoining',
            field=models.DateField(blank=True, null=True),
        ),
    ]
