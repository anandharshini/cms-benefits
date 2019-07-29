from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

def upload_location(instance, filename):
    return "%s/%s" %(instance.submit_user, filename)

class ApplicationModel(models.Model):
    name = models.ForeignKey("core.LookupModel", verbose_name=_("Forms"), on_delete=models.CASCADE)
    submit_user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    employee = models.ForeignKey("healthquestionaire.EmployeeModel", verbose_name=_(""), on_delete=models.CASCADE, blank=True, null=True)
    pdf_file = models.FileField(_("Application Form"), upload_to=upload_location, max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'pdf_forms_submitted'
    