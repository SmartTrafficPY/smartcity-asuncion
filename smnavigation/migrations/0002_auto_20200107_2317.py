# Generated by Django 2.2.4 on 2020-01-07 23:17

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smnavigation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='navigationrequest',
            name='route',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(blank=True, null=True),
                blank=True,
                default=list,
                null=True,
                size=None),
        ),
        migrations.AlterField(
            model_name='navigationrequest',
            name='score',
            field=models.IntegerField(
                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                help_text='1 lowest score, 5 highest score',
                null=True),
        ),
    ]
