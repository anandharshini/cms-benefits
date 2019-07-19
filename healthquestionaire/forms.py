from django import forms
from .models import HealthQuestionnaireModel, EmployeeModel, CoverageModel
from employer.models import Employer
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from django.forms import BaseModelFormSet
from django.contrib.admin import widgets 

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = ()

EmployerFormset = modelformset_factory(
    Employer, exclude=()
)

class EmployeeModelForm(forms.ModelForm):
    class Meta:
        model = EmployeeModel
        exclude = ()

class BaseEmployeeFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = EmployeeModel.objects.all()

EmployeeFormset = modelformset_factory(
    EmployeeModel, exclude=(), formset=BaseEmployeeFormSet
    )

class EmployeeForm(forms.Form):
    EMPLOYEE_GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
    )
    employer_name = forms.CharField(max_length=250, required=True)
    employer_steet_address = forms.CharField(max_length=250, required=False)
    employer_city = forms.CharField(max_length=100, required=False)
    employer_state = forms.CharField(max_length=50, required=False)
    employer_zip = forms.CharField(max_length=20, required=False)
    empl_full_name = forms.CharField(max_length=250, required=True)
    empl_hire_date = forms.DateTimeField(required=True, widget=forms.DateInput(attrs={'class': 'datepicker'}))
    empl_dob = forms.DateTimeField(required=False, widget=forms.DateInput(attrs={'class': 'datepicker'}))
    empl_steet_address = forms.CharField(max_length=250, required=False)
    empl_city = forms.CharField(max_length=100, required=False)
    empl_state = forms.CharField(max_length=50, required=False)
    empl_zip = forms.CharField(max_length=20, required=False)
    empl_ssn = forms.CharField(max_length=20, required=True)
    empl_gender = forms.ChoiceField(choices=EMPLOYEE_GENDER_CHOICES, required=False)

class CoverageForm(forms.ModelForm):
    
    class Meta:
        model = CoverageModel
        exclude = ()
        widgets = {
            'effective_date': forms.DateInput(attrs={'class': 'datepicker'})
        }

class HealthApplicationForm(forms.ModelForm):
    class Meta:
        model = EmployeeModel
        exclude = []

