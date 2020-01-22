# Generated by Django 2.2.4 on 2020-01-08 03:51

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smnavigation', '0002_auto_20200107_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navigationrequest',
            name='route',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.TextField(blank=True, null=True),
                blank=True,
                default=list,
                null=True,
                size=None),
        ),
    ]
