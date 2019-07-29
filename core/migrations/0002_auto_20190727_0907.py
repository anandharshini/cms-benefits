# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-27 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('healthquestionaire', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeedependent',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='healthquestionaire.EmployeeModel', verbose_name='Employee'),
        ),
        migrations.AddField(
            model_name='employeedependent',
            name='gender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empl_gender', to='core.LookupModel', verbose_name='Gender'),
        ),
        migrations.AddField(
            model_name='employeedependent',
            name='relationship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empl_relationship', to='core.LookupModel', verbose_name='Relationship to Employee'),
        ),
        migrations.AddField(
            model_name='address',
            name='address_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.LookupModel', verbose_name='Address Type'),
        ),
    ]
