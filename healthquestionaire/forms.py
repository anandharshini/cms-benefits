from django import forms
from .models import HealthQuestionnaireModel, EmployeeModel, CoverageModel, MedicalModel, MedicationModel, DependentInfoModel
from employer.models import Employer
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from django.forms import formset_factory 
from core.utils import CombinedFormBase
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
    class Meta:
        model = EmployeeModel
        exclude = ('all_forms_complete', 'login_user', 'current_url', 'form_type',)
        widgets = {
            'empl_hire_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'empl_dob': forms.DateInput(attrs={'class': 'datepicker'})
        }
    
    def __init__(self, *args, **kwargs):
        super(EmployeeModelForm, self).__init__(*args, **kwargs)
        self.fields['empl_gender'].queryset = LookupModel.objects.filter(type_lookup='gender')
        self.fields['marital_status'].queryset = LookupModel.objects.filter(type_lookup='marital_status')
    

class CoverageForm(forms.ModelForm):    
    class Meta:
        model = CoverageModel
        exclude = ()
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
        self.fields['coverage'].queryset = LookupModel.objects.filter(type_lookup='coverage_resp')
        self.fields['coverage_level'].queryset = LookupModel.objects.filter(type_lookup='coverage_level')
        self.fields['decline_reasons'].queryset = LookupModel.objects.filter(type_lookup='decline_reason')

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
        exclude=()

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
    extra=1
)

MedicationModelFormset = modelformset_factory(
    MedicationModel,
    fields='__all__',
    extra=1
)

class MedicalModelForm(forms.ModelForm):
    class Meta:
        model = MedicalModel
        exclude=()
    
    def __init__(self, *args, **kwargs):
        pass

class MedicationModelForm(forms.ModelForm):
    class Meta:
        model = MedicationModel
        exclude=()
    
    def __init__(self, *args, **kwargs):
        pass
