from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class LookupModel(models.Model):
    key_lookup = models.CharField(_("Key"), max_length=150)
    value_lookup = models.CharField(_("Value"), max_length=450)
    type_lookup = models.CharField(_("Type"), max_length=50)
    class Meta:
        verbose_name = _("Lookup")
        verbose_name_plural = _("Lookup Data")
        unique_together = ('key_lookup', 'type_lookup')
        db_table = 'lookup_data'

    def __str__(self):
        return self.value_lookup
    
class Address(models.Model):
    address_type = models.ForeignKey("core.LookupModel", verbose_name=_("Address Type"), on_delete=models.CASCADE)
    street = models.CharField(_("Street"), max_length=50)
    address2 = models.CharField(_("address2"), max_length=150, blank=True, null=True)
    city = models.CharField(_("city"), max_length=150)
    state = models.CharField(_("state"), max_length=200)
    zip_code = models.CharField(_("zip_code"), max_length=50)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
    
    def __str__(self):
        return self.street

class HeightWeight(models.Model):
    height_feet = models.IntegerField(_("Feet"))
    height_inches = models.IntegerField(_("Inches"))
    weight_lbs = models.IntegerField(_("Weight in lbs"))

    class Meta:
        db_table = 'emp_height_weight'
    
    def __str__(self):
        return self.height_feet

class MedicalConditionsTreatment(models.Model):
    conditions = models.ManyToManyField("core.LookupModel", verbose_name=_("Conditions/Treatments"))

    class Meta:
        db_table = 'medical_conditions_treatments'
    
    def __init__(self, *args, **kwargs):
        super(Address, self).__init__(*args, **kwargs)
        self.conditions.queryset = LookupModel.objects.filter(type_lookup='medical_conditions')

    def __str__(self):
        return self.conditions.key_lookup

class EmployeeDependent(models.Model):
    first_name = models.CharField(_("First Name"), max_length=150)
    last_name = models.CharField(_("Last Name"), max_length=250)
    relationship = models.ForeignKey("core.LookupModel", related_name='empl_relationship', verbose_name=_("Relationship to Employee"), on_delete=models.CASCADE)
    ssn = models.CharField(_("Social Security Number"), max_length=10)
    dob_dependent = models.DateTimeField(_("Date of Birth"), auto_now=False, auto_now_add=False)
    age = models.IntegerField(_("Age"))
    gender = models.ForeignKey("core.LookupModel", related_name='empl_gender', verbose_name=_("Gender"), on_delete=models.CASCADE)
    tobacco_use = models.BooleanField(_("Tobacco Use"))
    employee = models.ForeignKey("healthquestionaire.EmployeeModel", verbose_name=_("Employee"), on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = _("Dependent")
        verbose_name_plural = _("Dependents")
        db_table ='employee_dependents'
    
    def __str__(self):
        return self.last_name
