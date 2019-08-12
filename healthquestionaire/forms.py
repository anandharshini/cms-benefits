from django import forms
from .models import HealthQuestionnaireModel, EmployeeModel, CoverageModel, MedicalModel, MedicationModel, DependentInfoModel
from employer.models import Employer
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django.forms import formset_factory 
from core.utils import CombinedFormBase, height_regex
from employer.forms import EmployerForm
from core.models import Address, EmployeeDependent, LookupModel
from django.forms import modelformset_factory


class AddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ()
    
    def __init__(self, *args, **kwargs):
        super(AddressModelForm, self).__init__(*args, **kwargs)
        self.fields['address_type'].queryset = LookupModel.objects.filter(type_lookup='address_type')

class EmployeeModelForm(forms.ModelForm):
    # empl_dob = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    # empl_hire_date = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = EmployeeModel
        exclude = ('all_forms_complete', 'login_user', 'current_url', 'form_type',)
        # fields = ('')
        widgets = {
            #  'empl_hire_date': forms.DateInput(attrs={'class': 'datepicker'}),
            #  'empl_dob': forms.DateInput(attrs={'class': 'datepicker'}),
             'empl_ssn': forms.TextInput(attrs={'class': 'masked', 'pattern': '^([1-9])(?!\1{2}-\1{2}-\1{4})[1-9]{2}-[1-9]{2}-[1-9]{4}$', 'placeholder': '999-99-9999'}),
             'zip_code': forms.TextInput(attrs={'class': 'masked', 'pattern': '^\d{5}-\d{4}|\d{5}|[A-Z]\d[A-Z] \d[A-Z]\d$', 'placeholder': '99999-9999'}),
             'home_phone': forms.TextInput(attrs={'class': 'masked', 'pattern': '^[2-9]\d{2}-\d{3}-\d{4}$', 'placeholder': '999-999-9999'}),
             'cell_phone': forms.TextInput(attrs={'class': 'masked', 'pattern': '^[2-9]\d{2}-\d{3}-\d{4}$', 'placeholder': '999-999-9999'}),
             'empl_dob': forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'masked', 'pattern': '^(((0?[1-9]|1[012])/(0?[1-9]|1\d|2[0-8])|(0?[13456789]|1[012])/(29|30)|(0?[13578]|1[02])/31)/(19|[2-9]\d)\d{2}|0?2/29/((19|[2-9]\d)(0[48]|[2468][048]|[13579][26])|(([2468][048]|[3579][26])00)))$', 'placeholder': 'MM/dd/yyyy'}),
             'empl_hire_date': forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'masked', 'pattern': '^(((0?[1-9]|1[012])/(0?[1-9]|1\d|2[0-8])|(0?[13456789]|1[012])/(29|30)|(0?[13578]|1[02])/31)/(19|[2-9]\d)\d{2}|0?2/29/((19|[2-9]\d)(0[48]|[2468][048]|[13579][26])|(([2468][048]|[3579][26])00)))$', 'placeholder': 'MM/dd/yyyy'})
            #'empl_dob': forms.DateTimeField(input_formats=['%d/%m/%y'])
                    }
    
    def __init__(self, *args, **kwargs):
        super(EmployeeModelForm, self).__init__(*args, **kwargs)
        self.fields['empl_gender'].queryset = LookupModel.objects.filter(type_lookup='gender')
        self.fields['marital_status'].queryset = LookupModel.objects.filter(type_lookup='marital_status')
        self.fields['hours_worked_per_week'].queryset = LookupModel.objects.filter(type_lookup='hours_worked')
        self.fields['state'].queryset = LookupModel.objects.filter(type_lookup='us_states')

class CoverageForm(forms.ModelForm):    
    class Meta:
        model = CoverageModel
        exclude = ('employee',)
        widgets = {
            'effective_date': forms.DateInput(attrs={'class': 'datepicker'}),
            # 'tobacco_use': forms.RadioSelect,
            # 'dependent_disabled': forms.RadioSelect,
            # 'coverage': forms.RadioSelect,
            # 'decline_reasons': forms.CheckboxSelectMultiple,
            # 'dependent_insurance_other_continue': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        super(CoverageForm, self).__init__(*args, **kwargs)
        self.fields['tobacco_use'].queryset = LookupModel.objects.filter(type_lookup='yes_no')
        self.fields['dependent_disabled'].queryset = LookupModel.objects.filter(type_lookup='yes_no')
        self.fields['dependent_insurance_other_continue'].queryset = LookupModel.objects.filter(type_lookup='yes_no')
        # self.fields['coverage'].queryset = LookupModel.objects.filter(type_lookup='coverage_resp')
        self.fields['coverage_level'].queryset = LookupModel.objects.filter(type_lookup='coverage_level')
        # self.fields['decline_reasons'].queryset = LookupModel.objects.filter(type_lookup='decline_reason')

class HealthApplicationForm(forms.ModelForm):
    class Meta:
        model = EmployeeModel
        exclude = []

class EmployerAddressForm(CombinedFormBase):
    form_classes = [EmployerForm, AddressModelForm]

class EmployeeAddressForm(CombinedFormBase):
    form_classes = [EmployeeModelForm, AddressModelForm]

class DependentInfoForm(forms.ModelForm):
    class Meta:
        model = DependentInfoModel
        exclude=('employee', 'self_height_inches', 'spouse_height_inches')
        widgets = {
            'self_height_feet': forms.TextInput(attrs={'class': 'masked', 'pattern': '^(\d{1,2})[\']?((\d)|([0-1][0-2]))?[\"]?$', 'placeholder': '9\'99\"'}),
            'spouse_height_feet': forms.TextInput(attrs={'class': 'masked', 'pattern': '^(\d{1,2})[\']?((\d)|([0-1][0-2]))?[\"]?$', 'placeholder': '9\'99\"'}), 
            'self_weight_lbs': forms.TextInput(attrs={'class': 'masked', 'pattern': '^[0-9][0-9][0-9]$', 'placeholder': '999'}),
            'spouse_weight_lbs': forms.TextInput(attrs={'class': 'masked', 'pattern': '^[0-9][0-9][0-9]$', 'placeholder': '999'})
        }

    def __init__(self, *args, **kwargs):
        super(DependentInfoForm, self).__init__(*args, **kwargs)
        self.fields['diagnose_treated'].queryset = LookupModel.objects.filter(type_lookup='med_conditions')
        self.fields['past_5_insu_decl'].queryset = LookupModel.objects.filter(type_lookup='yes_no')
        self.fields['past_24_med_cond'].queryset = LookupModel.objects.filter(type_lookup='yes_no')
        self.fields['past_24_mon_med_exp_5k'].queryset = LookupModel.objects.filter(type_lookup='yes_no')
        self.fields['anticipate_hozpital'].queryset = LookupModel.objects.filter(type_lookup='yes_no')
        self.fields['dependent_pregnant'].queryset = LookupModel.objects.filter(type_lookup='yes_no')

MedicalModelFormset = modelformset_factory(
    MedicalModel,
    fields='__all__',
    widgets = {
        'date_of_onset': forms.TextInput(attrs={'class': 'masked', 'pattern': '^((\d)|([0-9][0-9]))[\/]?((\d)|([0-9][0-9][0-9][0-9]))?$', 'placeholder': 'MM/yyyy'}),
        'date_last_seen': forms.TextInput(attrs={'class': 'masked', 'pattern': '^((\d)|([0-9][0-9]))[\/]?((\d)|([0-9][0-9][0-9][0-9]))?$', 'placeholder': 'MM/yyyy'})
    },
    extra=1
)

MedicationModelFormset = modelformset_factory(
    MedicationModel,
    fields='__all__',
    extra=1
)

# class MedicalModelForm(forms.ModelForm):
#     class Meta:
#         model = MedicalModel
#         exclude = ()
#         widgets = {
#             'date_of_onset': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'masked', 'pattern': '^(((0?[1-9]|1[012])/(0?[1-9]|1\d|2[0-8])|(0?[13456789]|1[012])/(29|30)|(0?[13578]|1[02])/31)/(19|[2-9]\d)\d{2}|0?2/29/((19|[2-9]\d)(0[48]|[2468][048]|[13579][26])|(([2468][048]|[3579][26])00)))$', 'placeholder': 'MM/yyyy'}),
#             'date_last_seen': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'masked', 'pattern': '^(((0?[1-9]|1[012])/(0?[1-9]|1\d|2[0-8])|(0?[13456789]|1[012])/(29|30)|(0?[13578]|1[02])/31)/(19|[2-9]\d)\d{2}|0?2/29/((19|[2-9]\d)(0[48]|[2468][048]|[13579][26])|(([2468][048]|[3579][26])00)))$', 'placeholder': 'MM/yyyy'})
#         }
    
#     def __init__(self, *args, **kwargs):
#         pass

# class MedicationModelForm(forms.ModelForm):
#     class Meta:
#         model = MedicationModel
#         exclude=()
    
#     def __init__(self, *args, **kwargs):
#         pass
