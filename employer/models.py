from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Employer(models.Model):
    name = models.CharField(_("Employer Name"), max_length=250)
    ein = models.CharField(_("EIN"), max_length=150, blank=True, null=True)
    street = models.CharField(_("Street"), max_length=50)
    address2 = models.CharField(_("address2"), max_length=150, blank=True, null=True)
    city = models.CharField(_("city"), max_length=150)
    state = models.CharField(_("state"), max_length=200)
    zip_code = models.CharField(_("zip_code"), max_length=50)
    # employee = models.ManyToManyField("healthquestionaire.EmployeeModel", verbose_name=_("Employee Employer Relation"))
    
    class Meta:
        db_table = 'employers'
    
    def __str__(self):
        return self.name