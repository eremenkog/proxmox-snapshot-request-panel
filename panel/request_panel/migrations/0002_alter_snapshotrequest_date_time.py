# Generated by Django 5.1 on 2024-09-10 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snapshotrequest',
            name='date_time',
            field=models.CharField(max_length=255),
        ),
    ]
