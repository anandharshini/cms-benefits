# Generated by Django 2.1.5 on 2019-08-23 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('form_application', '0002_applicationmodel_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationmodel',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application_form_type', to='core.LookupModel', verbose_name='Forms'),
        ),
        migrations.AlterField(
            model_name='applicationmodel',
            name='pdf_file',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Url PDF'),
        ),
    ]