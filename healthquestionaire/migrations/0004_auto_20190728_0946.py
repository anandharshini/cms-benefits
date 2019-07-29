# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-28 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthquestionaire', '0003_auto_20190728_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coveragemodel',
            name='decline_reasons',
            field=models.ManyToManyField(blank=True, related_name='reasons_for_decline', to='core.LookupModel', verbose_name='Reason for Decline'),
        ),
        migrations.AlterField(
            model_name='coveragemodel',
            name='dependent_isu_coverage_carrier',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='If Yes, name of Carrier'),
        ),
    ]
