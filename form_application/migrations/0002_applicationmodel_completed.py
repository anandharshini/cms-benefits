# Generated by Django 2.1.5 on 2019-08-16 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form_application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationmodel',
            name='completed',
            field=models.NullBooleanField(verbose_name='PDF Form Completed'),
        ),
    ]
