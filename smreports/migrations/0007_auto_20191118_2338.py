# Generated by Django 2.2.4 on 2019-11-18 23:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smreports', '0006_reportpoi_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReportPoi',
            new_name='Report',
        ),
        migrations.RenameModel(
            old_name='Contribution',
            new_name='StatusUpdate',
        ),
        migrations.RenameField(
            model_name='report',
            old_name='coordinates_poi',
            new_name='coordinates',
        ),
        migrations.RenameField(
            model_name='statusupdate',
            old_name='reportpoi',
            new_name='reportid',
        ),
        migrations.AlterUniqueTogether(
            name='statusupdate',
            unique_together={('reportid', 'user', 'value')},
        ),
    ]
