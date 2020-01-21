# Generated by Django 2.2.4 on 2020-01-09 00:28

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smnavigation', '0003_auto_20200108_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='navigationrequest',
            name='report_light',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(blank=True, null=True),
                blank=True,
                default=list,
                null=True,
                size=None),
        ),
        migrations.AddField(
            model_name='navigationrequest',
            name='report_severe',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(blank=True, null=True),
                blank=True,
                default=list,
                null=True,
                size=None),
        ),
    ]