from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms
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
        return self.empl_first_name + ' ' + self.empl_last_name

class EmployeeModel(models.Model):
    fk_employer = models.ForeignKey("employer.Employer", verbose_name=_("Employer"), related_name='employerName', on_delete=models.CASCADE)
    empl_hire_date = models.DateField(_("* Hire Date"), auto_now_add=False, auto_now=False)
    job_title = models.CharField(_("* Job Title"), max_length=150)
    hours_worked_per_week = models.ForeignKey("core.LookupModel", verbose_name=_("* Working Status (30 hrs or more is Full Time)"), related_name='empl_hours_wored', on_delete=models.CASCADE)
    empl_first_name = models.CharField(_("* First Name"), max_length=250)
    empl_last_name = models.CharField(_("* Last Name"), max_length=250)
    empl_dob = models.DateField(_("* DOB"), auto_now=False, auto_now_add=False)
    empl_ssn = models.CharField(max_length=11, verbose_name=_("* SSN"))
    empl_gender = models.ForeignKey("core.LookupModel", verbose_name=_("* Gender"), related_name='empl_gender_lookupmodel', on_delete=models.CASCADE)
    marital_status = models.ForeignKey("core.LookupModel", verbose_name=_("* Marital status"), related_name='empl_marital_status', on_delete=models.CASCADE)
    street = models.CharField(_("* Address 1"), max_length=50)
    address2 = models.CharField(_("Address 2"), max_length=150, blank=True, null=True)
    city = models.CharField(_("* city"), max_length=150)
    state = models.ForeignKey("core.LookupModel", verbose_name=_("* State"), related_name='empl_state', on_delete=models.CASCADE)
    zip_code = models.CharField(_("* Zip"), max_length=50)
    email_address = models.EmailField(_("Email"), max_length=254, blank=True, null=True)
    home_phone = models.CharField(_("Home Phone"), max_length=50, blank=True, null=True)
    cell_phone = models.CharField(_("Cell Phone"), max_length=50, blank=True, null=True)
    spouse_employer = models.CharField(_("Spouse's Employer"), max_length=150, blank=True, null=True)
    spouse_buisness_phone = models.CharField(_("Spouse's Buisness Phone"), max_length=50, blank=True, null=True)
    form_type = models.ManyToManyField("core.LookupModel", verbose_name=_("Form Type"), related_name='empl_form_type', default=40)
    login_user = models.ForeignKey(User, verbose_name=_("Logged In User"), on_delete=models.CASCADE, blank=True, null=True)
    current_url = models.CharField(_("User in This Page"), max_length=150, blank=True, null=True)
    all_forms_complete = models.BooleanField(_("All Forms Completed"), default=False)

    class Meta:
        db_table = 'employees'
    def __str__(self):
        return self.empl_first_name + ' ' + self.empl_last_name

class CoverageModel(models.Model):
    coverage_level = models.ForeignKey("core.LookupModel", related_name='coverage_level', verbose_name=_("* Coverage Level"), on_delete=models.CASCADE)
    employee = models.ForeignKey("healthquestionaire.EmployeeModel", verbose_name=_("Employee"), on_delete=models.CASCADE)
    tobacco_use = models.ForeignKey("core.LookupModel", verbose_name=_("* Tobacco Use"), related_name='employee_tobacco_use', on_delete=models.CASCADE)
    dependent_disabled = models.ForeignKey("core.LookupModel", related_name='empl_dependent_disabled', verbose_name=_("* Are you or any dependent(s) disabled?"), on_delete=models.CASCADE)
    dependent_disabled_name = models.CharField(_("If Yes please indicate name(s)"), max_length=250, blank=True, null=True)
    
    dependent_insurance_other_continue = models.ForeignKey("core.LookupModel", related_name='empl_depend_other_insu_coverage', verbose_name=_("* Do you or any of your family have other health insurance that will continue in addition to this coverage?"), on_delete=models.CASCADE)
    dependent_isu_coverage_carrier = models.CharField(_("If Yes, Other Coverage Carrier Name"), max_length=250, blank=True, null=True)
    policy_holders_name = models.CharField(_("If Yes, Other Coverage Policy Holder's Name"), max_length=50, blank=True, null=True)
    policy_number = models.CharField(_("If Yes, Other Coverage Policy Number"), max_length=50, blank=True, null=True)
    effective_date = models.DateField(_("If Yes, Other Coverage Effective Policy Date"), auto_now=False, auto_now_add=False, blank=True, null=True)
    # coverage = models.ForeignKey("core.LookupModel", verbose_name=_("Accept/Decline"), related_name='empl_coverage_accept', on_delete=models.CASCADE)
    # decline_reasons = models.ManyToManyField("core.LookupModel", related_name='reasons_for_decline', verbose_name=_("Reason for Decline"), blank=True)
    # others = models.CharField(_("Others"), max_length=150, blank=True, null=True)
    names_covered_dependents = models.CharField(_("If Yes, Name(s) Of Covered Dependents"), max_length=550, blank=True, null=True)

    def __str__(self):
        return self.policy_holders_name

class MedicalModel(models.Model):
    family_member = models.CharField(_("Family Member"), max_length=250)
    disease_diag_treat = models.CharField(_("Disease/Diagnosis/Treatment"), max_length=250)
    date_of_onset = models.CharField(_("Date Of Onset"), max_length=50)
    date_last_seen = models.CharField(_("Date Last Seen By Physician"), max_length=50)
    remaining_symp_probs = models.CharField(_("Remaining Symptoms Or Problems"), max_length=500)
    employee = models.ForeignKey("healthquestionaire.EmployeeModel", verbose_name=_(""), on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.family_member

class MedicationModel(models.Model):
    family_member = models.CharField(_("Family Member"), max_length=250)
    medication_rx_injection = models.CharField(_("Medication/Rx/Injection"), max_length=250)
    dosage = models.CharField(_("Dosage"), max_length=50)
    med_condition = models.CharField(_("Medical Condition"), max_length=350)
    employee = models.ForeignKey("healthquestionaire.EmployeeModel", verbose_name=_(""), on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.family_member

class DependentInfoModel(models.Model):
    employee = models.ForeignKey("healthquestionaire.EmployeeModel", verbose_name=_("For Employee"), on_delete=models.CASCADE)
    self_height_feet = models.CharField(_("* Self Height"), max_length=50)
    self_height_inches = models.CharField(_("Self-Height (inches)"), max_length=50, blank=True, null=True)
    self_weight_lbs = models.CharField(_("* Self Weight (lbs)"), max_length=50)
    spouse_height_feet = models.CharField(_("Spouse Height"), max_length=50, blank=True, null=True)
    spouse_height_inches = models.CharField(_("Spouse-Height (inches)"), max_length=50, blank=True, null=True)
    spouse_weight_lbs = models.CharField(_("Spouse Weight (lbs)"), max_length=50, blank=True, null=True)
    diagnose_treated = models.ManyToManyField("core.LookupModel", blank=True, related_name='dep_diagnose_treated', verbose_name=_("""Have you or any of your dependent(s) been diagnosed or treated for, or has hospitalization or surgery not yet performed been
        recommended for, any of the following conditions in the past five (5) years? If so, the plan requires you to disclose these conditions solely
        for underwriting purposes (and you can properly disclose by checking “Yes” for each of the conditions for which you and/or your
        dependents have previously received diagnosis, treatment or a recommendation for hospitalization or surgery not yet performed).
        Although neither you nor your dependents will be denied coverage because of any previous treatment, diagnosis or recommendation for
        hospitalization or surgery not yet performed for any condition, if you fail to disclose any previous treatment, diagnosis, recommendation
        of hospitalization or surgery not yet performed for a condition listed below, the health plan will not cover any medical expenses, diagnosis,
        treatment, services, supplies, surgeries or hospitalizations for that undisclosed condition related or attributable, to the coverage sought
        as part of this application. NOTE: You are required to disclose any updates to these health questions that may arise prior to the effective date of your coverage"""))
    past_5_insu_decl = models.ForeignKey("core.LookupModel", related_name='dep_past_5_ins_decl', verbose_name=_("""* Within the past 5 years, have you or any dependent ever had an application for insurance declined, postponed,
        rated or otherwise modified?"""), on_delete=models.CASCADE)
    past_24_med_cond = models.ForeignKey("core.LookupModel", related_name='dep_past_24_med_cond', verbose_name=_("""* Have you or any of your dependent(s) had any medical conditions in the past 24 months requiring medical care,
        prescription management, surgery, or hospitalization? * If Yes, please provide information on who and for what conditions in space provided below"""), on_delete=models.CASCADE)
    past_24_mon_med_exp_5k = models.ForeignKey("core.LookupModel", related_name='dep_past_24_mon_med_exp_5k', verbose_name=_("""* In the past 24 months, have you or any of your dependent(s) had more than $5,000 in medical expenses? * If Yes, please provide information on who and for what medical conditions in space provided below"""), on_delete=models.CASCADE)
    anticipate_hozpital = models.ForeignKey("core.LookupModel", related_name='dep_anticipate_hozpital', verbose_name=_("""* Are you or any of your dependent(s) anticipating hospitalization or surgery, or had surgery or hospitalization
recommended that has not been performed? * If Yes, please provide information below"""), on_delete=models.CASCADE)
    dependent_pregnant = models.ForeignKey("core.LookupModel", related_name='dep_dependent_pregnant', verbose_name=_("""* Are you or any dependent(s) currently pregnant or suspect you / they may be pregnant? * If Yes, please provide due date and detail in space provided below"""), on_delete=models.CASCADE)
