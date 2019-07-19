from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Employer(models.Model):
    name = models.CharField(max_length=250)
    employer_address = models.ForeignKey("core.Address", verbose_name=_("EmployerAddress"), related_name='employer_address', db_column='employer_address', on_delete=models.CASCADE)

    class Meta:
        db_table = 'employers'
    
    def __str__(self):
        return self.name