# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-04 21:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthquestionaire', '0010_auto_20190804_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coveragemodel',
            name='dependent_isu_coverage_carrier',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='If Yes, Other Coverage Carrier Name'),
        ),
        migrations.AlterField(
            model_name='coveragemodel',
            name='effective_date',
            field=models.DateField(blank=True, null=True, verbose_name='If Yes, Other Coverage Effective Policy Date'),
        ),
        migrations.AlterField(
            model_name='coveragemodel',
            name='names_covered_dependents',
            field=models.CharField(blank=True, max_length=550, null=True, verbose_name='If Yes, Other Coverage Name(s) Of Covered Dependents'),
        ),
        migrations.AlterField(
            model_name='coveragemodel',
            name='policy_holders_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="If Yes, Other Coverage Policy Holder's Name"),
        ),
        migrations.AlterField(
            model_name='coveragemodel',
            name='policy_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='If Yes, Other Coverage Policy Number'),
        ),
    ]