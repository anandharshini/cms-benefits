# Generated by Django 2.1.5 on 2019-08-23 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form_application', '0003_auto_20190823_0756'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicationmodel',
            old_name='name',
            new_name='form_name',
        ),
    ]