from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

def upload_location(instance, filename):
    return "%s/%s" %(instance.submit_user.id, filename)

class ApplicationModel(models.Model):

    submit_user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    pdf_file = models.FileField(_("Application Form"), upload_to=upload_location, max_length=100)

    class Meta:
        db_table = 'pdf_forms_submitted'
    
    def __str__(self):
        return self.submit_user.id
    
