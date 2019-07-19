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

class Address(models.Model):
    ADDRESS_TYPE_CHOICES = (
        ('PHYSICAL', 'Physical Address'),
        ('MAIL', 'Mailing Address'),
    )
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    street = models.CharField(_("street"), max_length=50, blank=True)
    address2 = models.CharField(_("address2"), max_length=150, blank=True)
    city = models.CharField(_("city"), max_length=150, blank=True)
    state = models.CharField(_("state"), max_length=200, blank=True)
    zip_code = models.CharField(_("zip_code"), max_length=50, blank=True)

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

class MedicalConditionsTreatment(models.Model):
    MEDICAL_CONDITIONS_CHOICES = (
        ('CARDIAC_DISORDER', 'Cardiac Disorder'),
        ('CANCER_TUMOR_ANY_FORM', 'Cancer Tumor (any form)'),
        ('DIABETES', 'Diabetes'),
        ('KIDNEY_DISORDER', 'Kidney Disorder'),
    )
    conditions = models.CharField(_("Conditions/Treatments"), max_length=50, choices=MEDICAL_CONDITIONS_CHOICES)

    class Meta:
        db_table = 'medical_conditions_treatments'

class EmployeeDependent(models.Model):
    RELATIONSHIP_CHOICES = (
        ('SPOUSE', 'SPOUSE'),
        ('SON', 'SON'),
        ('DAUGHTER', 'DAUGHTER'),
    )
    first_name = models.CharField(_("First Name"), max_length=150)
    last_name = models.CharField(_("Last Name"), max_length=250)
    relationship = models.CharField(_("Relationship to Employee"), max_length=10, choices=RELATIONSHIP_CHOICES)
    ssn = models.CharField(_("Social Security Number"), max_length=10)
    dob_dependent = models.DateTimeField(_("Date of Birth"), auto_now=False, auto_now_add=False)
    age = models.IntegerField(_("Age"))
    gender = models.CharField(max_length=50)
    tobacco_use = models.BooleanField(_("Tobacco Use"))
    
    class Meta:
        verbose_name = _("Dependent")
        verbose_name_plural = _("Dependents")
        db_table ='employee_dependents'
