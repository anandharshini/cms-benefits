from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

TOBACCO_USE_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No'),
)
COVERAGE_CHOICES = (
    ('DECLINE', 'I Decline Coverage'),
    ('ACCEPT', 'I Accept Coverage'),
)
COVERAGE_LEVEL_CHOICES = (
    ('EMP_ONLY', 'EMPLOYEE ONLY'),
    ('EMP_SPOUSE', 'EMPLOYEE / SPOUSE'),
    ('EMP_CHILDREN', 'EMPLOYEE / CHILDREN'),
    ('FAMILY', 'FAMILY'),
)
REASON_FOR_DECLINE_CHOICES = (
    ('SP_EMP_PLAN', 'SPOUSE\'S EMPLOYER\'S PLAN'),
    ('IND_PLAN', 'INDIVIDUAL PLAN'),
    ('MEDICARE', 'MEDICARE'),
    ('MEDICAID', 'MEDICAID'),
    ('COBRA_PREV_EMP', 'COBRA FROM PREVIOUS EMPLOYER'),
    ('VA_ELIG', 'VA ELIGIBILITY'),
    ('NO_COVERAGE_NOW', 'I HAVE NO COVERAGE AT THIS TIME'),
    ('OTHERS', 'OTHERS'),
)

# Create your models here.
class HealthQuestionnaireModel(models.Model):
    employee = models.ForeignKey("healthquestionaire.EmployeeModel", verbose_name=_("Employee"), on_delete=models.CASCADE)

    class Meta:
        db_table = 'health_questionnaire'

    def __str__(self):
        return self.employee.username

class EmployeeModel(models.Model):
    employer = models.ForeignKey("employer.Employer", verbose_name=_("Employer Info"), on_delete=models.CASCADE)
    employee = models.ForeignKey(User, verbose_name=_("Employee"), on_delete=models.CASCADE)
    empl_dependents = models.ForeignKey("core.EmployeeDependent", verbose_name=_("Dependents"), on_delete=models.CASCADE, blank=True, null=True)

class CoverageModel(models.Model):
    tobacco_use = models.CharField(_("Does tobacco use affect the rates?"), choices=TOBACCO_USE_CHOICES, max_length=10, blank=True, null=True)
    dependent_disabled = models.CharField(_("Are you or any dependent(s) disabled?"), choices=TOBACCO_USE_CHOICES, max_length=10, blank=True, null=True)
    dependent_disabled_name = models.CharField(_("If Yes please indicate name(s)"), max_length=250, blank=True, null=True)
    dependent_insurance_other_continue = models.CharField(_("Do you or your dependents have other health coverage?"), choices=TOBACCO_USE_CHOICES, max_length=10, blank=True, null=True)
    policy_holders_name = models.CharField(_("Policy Holder's Name"), max_length=50)
    policy_number = models.CharField(_("Policy Number"), max_length=50)
    effective_date = models.DateField(_("Effective Policy Date"), auto_now=False, auto_now_add=False)
    coverage = models.CharField(_("coverage"), max_length=50, choices=COVERAGE_CHOICES, default='ACCEPT')
    decline_reasons = models.CharField(_("Reason for Decline"), max_length=50, choices=REASON_FOR_DECLINE_CHOICES, blank=True, null=True)
    others = models.CharField(_("Others"), max_length=150, blank=True, null=True)
    self_height_weight = models.ForeignKey("core.HeightWeight", verbose_name=_("Self"), related_name="self_height_weight", on_delete=models.CASCADE, blank=True, null=True)
    spouse_height_weight = models.ForeignKey("core.HeightWeight", verbose_name=_("Spouse"), related_name="spouse_height_weight", on_delete=models.CASCADE, blank=True, null=True)
